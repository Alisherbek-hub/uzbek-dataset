# C Dasturlash Tili — 19-Qism: Mikrokontrollerlar va O'rnatilgan Tizimlar (Embedded C)
## (901-950 gacha bo'lgan amaliy topshiriqlar, kodlar va tushuntirishlar)

Ushbu to'plam quyidagi muhim mavzularni qamrab oladi:
* volatile kalit so'zi va Memory-Mapped I/O (MMIO)
* Bit manipulyatsiyasi va CMSIS registrlar xaritalashi
* GPIO boshqaruvi, BSRR atomik operatsiyasi va Debounce filtri
* Uzilishlar (Interrupts / ISR qoidalari) va PWM modulyatsiyasi
* UART, SPI va I2C protokollari drayverlari simulyatsiyasi
* ADC harakatlanuvchi filtr, Watchdog taymeri va Fixed-point arxitekturasi
* Avtonom Bort Datchiklar Tizimi Master Loyihasi

---

# 901-Topshiriq: volatile kalit so'zi va apparat registrlari (MMIO)

## Topshiriq sharti:
Nima uchun apparat registrlari volatile ko'rsatkichlar orqali e'lon qilinishi shartligini tushuntirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

// Apparat registri xotira manzili simulyatsiyasi
static uint32_t soxta_registr = 0;
#define STATUS_REG (*(volatile uint32_t*)&soxta_registr)

int main(void) {
    STATUS_REG = 0x01; // Qurilma ishga tushdi

    printf("Registr qiymati: 0x%02X\n", STATUS_REG);

    STATUS_REG |= 0x02; // Yangi bayroq qo'shildi
    printf("Yangilangan registr: 0x%02X\n", STATUS_REG);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. volatile kompilyatorga ushbu o'zgaruvchi dastur kodidan tashqarida (apparat ta'minoti yoki uzilish tomonidan) o'zgarishi mumkinligini bildiradi.
2. Kompilyator volatile o'zgaruvchini CPU registriga keshlashdan saqlanadi va har safar xotiradan yangitdan o'qiydi.

## Ishlash natijasi:
```text
Registr qiymati: 0x01
Yangilangan registr: 0x03
```

---

# 902-Topshiriq: Embedded C da Bit manipulyatsiyasi makroslari to'plami

## Topshiriq sharti:
SET, CLEAR, TOGGLE va CHECK amallarini registrlar ustida bajaruvchi asosiy makroslar.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define BIT(n)              (1UL << (n))
#define SET_BIT(reg, n)     ((reg) |= BIT(n))
#define CLEAR_BIT(reg, n)   ((reg) &= ~BIT(n))
#define TOGGLE_BIT(reg, n)  ((reg) ^= BIT(n))
#define READ_BIT(reg, n)    (((reg) >> (n)) & 1UL)

int main(void) {
    uint32_t gpio = 0; // Barcha pinlar o'chiq

    SET_BIT(gpio, 5); // 5-pin yoqildi
    printf("Pin 5 yoqildi: 0x%02X\n", gpio);

    TOGGLE_BIT(gpio, 5); // 5-pin o'chirildi
    printf("Pin 5 teskari qilindi: 0x%02X\n", gpio);

    SET_BIT(gpio, 3);
    printf("Pin 3 holati: %lu\n", READ_BIT(gpio, 3));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mikrokontrollerlarda har bir oyoqcha (pin) bitta bitga to'g'ri keladi.
2. 1UL dan foydalanish 32-bitli arxitekturalarda to'g'ri siljishni ta'minlaydi.

## Ishlash natijasi:
```text
Pin 5 yoqildi: 0x20
Pin 5 teskari qilindi: 0x00
Pin 3 holati: 1
```

---

# 903-Topshiriq: Memory-Mapped I/O (MMIO): Registr manziliga to'g'ridan-to'g'ri ko'rsatkich

## Topshiriq sharti:
ARM Cortex-M arxitekturasidagi RCC va GPIO registrlarini C ko'rsatkichlari bilan bog'lash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

// Simulyatsiya qilingan apparat xotirasi
uint32_t ram_perif[2] = {0, 0};

#define PERIPH_BASE   ((uintptr_t)ram_perif)
#define GPIOA_MODER   (*(volatile uint32_t*)(PERIPH_BASE + 0x00))
#define GPIOA_ODR     (*(volatile uint32_t*)(PERIPH_BASE + 0x04))

int main(void) {
    // Pin 5 ni Output rejimiga o'rnatish (MODER[11:10] = 01)
    GPIOA_MODER |= (1UL << 10);
    // Pin 5 ga 1 (HIGH) chiqarish
    GPIOA_ODR |= (1UL << 5);

    printf("GPIOA MODER: 0x%08X\n", GPIOA_MODER);
    printf("GPIOA ODR:   0x%08X (Pin 5 HIGH)\n", GPIOA_ODR);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. MMIO da periferiya registrlari oddiy RAM xotira manzillari sifatida ko'rinadi.
2. C tili ko'rsatkichlari bu manzillarga to'g'ridan-to'g'ri murojaat qilish uchun ideal vositadir.

## Ishlash natijasi:
```text
GPIOA MODER: 0x00000400
GPIOA ODR:   0x00000020 (Pin 5 HIGH)
```

---

# 904-Topshiriq: Struktura orqali Periferiya Registrlarini xaritalash (CMSIS uslubi)

## Topshiriq sharti:
ARM CMSIS standartidagi kabi GPIO_TypeDef strukturasi bilan registrlarni qulay boshqarish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    volatile uint32_t MODER;   // Rejim registri (offset 0x00)
    volatile uint32_t OTYPER;  // Chiqish turi (offset 0x04)
    volatile uint32_t OSPEEDR; // Tezlik registri (offset 0x08)
    volatile uint32_t PUPDR;   // Pull-up/down (offset 0x0C)
    volatile uint32_t IDR;     // Kirish ma'lumotlari (offset 0x10)
    volatile uint32_t ODR;     // Chiqish ma'lumotlari (offset 0x14)
} GPIO_TypeDef;

GPIO_TypeDef soxta_gpio;
#define GPIOA ((GPIO_TypeDef *)&soxta_gpio)

int main(void) {
    GPIOA->MODER = 0x01;
    GPIOA->ODR = 0xFF;

    printf("MODER: 0x%X, ODR: 0x%X\n", GPIOA->MODER, GPIOA->ODR);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CMSIS (Cortex Microcontroller Software Interface Standard) struktura ichidagi maydonlar siljishini xotira offsetlariga 100% moslab joylashtiradi.

## Ishlash natijasi:
```text
MODER: 0x1, ODR: 0xFF
```

---

# 905-Topshiriq: Atomik Bit o'rnatish va tozalash: BSRR registri mexanizmi

## Topshiriq sharti:
ARM Cortex-M GPIO BSRR (Bit Set/Reset Register) yordamida uzilish xavfisiz atomik boshqaruv.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    volatile uint32_t ODR;
    volatile uint32_t BSRR;
} GPIO_Port;

GPIO_Port port = {0, 0};

void write_bsrr(uint32_t val) {
    port.BSRR = val;
    // Apparat mantiqi simulyatsiyasi:
    for (int i = 0; i < 16; i++) {
        if (val & (1UL << i)) port.ODR |= (1UL << i);          // Set
        if (val & (1UL << (i + 16))) port.ODR &= ~(1UL << i);   // Reset
    }
}

int main(void) {
    // Pin 13 ni yoqish (Quyi 16-bit: bit 13)
    write_bsrr(1UL << 13);
    printf("Pin 13 yoqildi: ODR = 0x%04X\n", port.ODR);

    // Pin 13 ni o'chirish (Yuqori 16-bit: bit 13+16)
    write_bsrr(1UL << (13 + 16));
    printf("Pin 13 o'chirildi: ODR = 0x%04X\n", port.ODR);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. BSRR registri Read-Modify-Write amallarini talab qilmaydi, bitta yozish bilan atomik tarzda pinni o'zgartiradi.
2. Bu uzilishlar (ISR) bilan yuzaga keladigan poyga holatlarini (race condition) to'liq bartaraf etadi.

## Ishlash natijasi:
```text
Pin 13 yoqildi: ODR = 0x2000
Pin 13 o'chirildi: ODR = 0x0000
```

---

# 906-Topshiriq: Tugma kontaktlari tebranishini filtrlash (Software Button Debounce)

## Topshiriq sharti:
Mexanik tugma bosilganda yuz beradigan mikrosekundlik shovqinlarni (bounce) dasturiy filtrlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint8_t holat;
    uint8_t sanagich;
} Tugma;

int yangila_tugma(Tugma *btn, uint8_t xom_signal) {
    if (xom_signal == btn->holat) {
        btn->sanagich = 0;
    } else {
        btn->sanagich++;
        if (btn->sanagich >= 5) { // 5 marta ketma-ket bir xil signal kelsa
            btn->holat = xom_signal;
            btn->sanagich = 0;
            return 1; // Holat o'zgardi!
        }
    }
    return 0;
}

int main(void) {
    Tugma t = {0, 0};
    uint8_t shovqin[] = {1, 0, 1, 1, 1, 1, 1}; // Tebranish va barqaror 1

    for (int i = 0; i < 7; i++) {
        if (yangila_tugma(&t, shovqin[i])) {
            printf("Tugma barqaror BOSILDI (bosqich %d)!\n", i);
        }
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mexanik metall kontaktlar ulangan paytda bir necha millisoniya davomida uzilib-ulanadi.
2. Debounce algoritmi bir necha qadam barqaror signal kutilgandagina tugma bosildi deb qabul qiladi.

## Ishlash natijasi:
```text
Tugma barqaror BOSILDI (bosqich 6)!
```

---

# 907-Topshiriq: Interrupt Service Routine (ISR) arxitekturasi va qoidalari

## Topshiriq sharti:
Apparat uzilishlari uchun yoziladigan C funksiyalari talablari (qisqa, xavfsiz va tezkor).

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

// ISR va asosiy dastur o'rtasidagi umumiy bayroq
volatile uint8_t uzilish_yuz_berdi = 0;

// Uzilish funksiyasi simulyatsiyasi
void EXTI0_IRQHandler(void) {
    // 1. Qisqa vaqt ichida faqat bayroq ko'tariladi
    uzilish_yuz_berdi = 1;
}

int main(void) {
    printf("Asosiy sikl ishlamoqda...\n");

    // Tashqi uzilish keldi deb hisoblaymiz
    EXTI0_IRQHandler();

    if (uzilish_yuz_berdi) {
        printf("[ASOSIY SIKL]: Uzilish qayd etildi, ma'lumotlar qayta ishlandi.\n");
        uzilish_yuz_berdi = 0;
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ISR qoidalari: hech qachon printf, malloc, erkin kutish (delay) ishlatilmaydi.
2. ISR faqat bayroqni o'rnatadi, asosiy og'ir hisoblash esa while(1) asosiy siklida bajariladi.

## Ishlash natijasi:
```text
Asosiy sikl ishlamoqda...
[ASOSIY SIKL]: Uzilish qayd etildi, ma'lumotlar qayta ishlandi.
```

---

# 908-Topshiriq: Kenglik-Impuls Modulyatsiyasi (PWM - Pulse Width Modulation)

## Topshiriq sharti:
Taymer hisoblagichi va solishtirish registri (CCR) orqali PWM signalini generatsiya qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint32_t ARR; // Auto-reload (Period: 100)
    uint32_t CCR; // Capture/Compare (Duty cycle: 25)
} TimerPWM;

uint8_t hisobla_pwm_chiqish(TimerPWM *tim, uint32_t joriy_hisob) {
    return (joriy_hisob < tim->CCR) ? 1 : 0;
}

int main(void) {
    TimerPWM pwm = { 100, 25 }; // 25% Duty Cycle

    printf("PWM to'lqini (25%% to'ldirish koeffitsienti):\n");
    for (uint32_t t = 0; t < 100; t += 10) {
        printf("t=%02u: %s | ", t, hisobla_pwm_chiqish(&pwm, t) ? "HIGH (1)" : "LOW  (0)");
        if (t == 40) printf("\n");
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. PWM raqamli mikrokontroller yordamida motor tezligini, LED yorug'ligini va isitkich quvvatini analogdek silliq boshqarish imkonini beradi.
2. Duty Cycle = (CCR / ARR) * 100%.

## Ishlash natijasi:
```text
PWM to'lqini (25% to'ldirish koeffitsienti):
t=00: HIGH (1) | t=10: HIGH (1) | t=20: HIGH (1) | t=30: LOW  (0) | t=40: LOW  (0) | 
t=50: LOW  (0) | t=60: LOW  (0) | t=70: LOW  (0) | t=80: LOW  (0) | t=90: LOW  (0) |
```

---

# 909-Topshiriq: UART Uzatish (Transmitter) drayveri simulyatsiyasi

## Topshiriq sharti:
Transmit Data Register (TDR) va Transmit Empty (TXE) bayrog'ini tekshirib bayt uzatish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    volatile uint32_t SR;  // Status Register (bit 7: TXE - bo'sh)
    volatile uint32_t DR;  // Data Register
} UART_Driver;

UART_Driver uart = { 0x80, 0 }; // TXE dastlab 1 (bo'sh)

void uart_send_char(char c) {
    // TXE 1 bo'lishini kutish (tayyor bo'lguncha)
    while (!(uart.SR & (1UL << 7)));
    uart.DR = (uint32_t)c;
    putchar(c); // Terminalga chiqarish
}

void uart_send_string(const char *s) {
    while (*s) uart_send_char(*s++);
}

int main(void) {
    printf("UART orqali xabar yuborilmoqda: ");
    uart_send_string("OK\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. UART apparat moduli baytni yuborib bo'lgach TXE bayrog'ini ko'taradi.
2. Drayver registr bo'shashini tekshirib keyingi baytni DR ga yozadi.

## Ishlash natijasi:
```text
UART orqali xabar yuborilmoqda: OK
```

---

# 910-Topshiriq: UART Qabul qilish uchun Halqasimon Bufer (UART RX Circular Buffer)

## Topshiriq sharti:
Uzilishda kelgan har bir baytni halqasimon buferga yig'ish va asosiy siklda o'qish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define RX_BUF_SIZE 8
volatile uint8_t rx_buf[RX_BUF_SIZE];
volatile uint8_t rx_head = 0, rx_tail = 0;

void USART_RX_ISR(uint8_t byte) {
    uint8_t next = (rx_head + 1) % RX_BUF_SIZE;
    if (next != rx_tail) {
        rx_buf[rx_head] = byte;
        rx_head = next;
    }
}

int uart_read_byte(uint8_t *out) {
    if (rx_head == rx_tail) return 0; // Bo'sh
    *out = rx_buf[rx_tail];
    rx_tail = (rx_tail + 1) % RX_BUF_SIZE;
    return 1;
}

int main(void) {
    // Uzilishlar simulyatsiyasi
    USART_RX_ISR('A');
    USART_RX_ISR('T');
    USART_RX_ISR('+');

    uint8_t c;
    printf("RX buferidan o'qilgan ma'lumotlar: ");
    while (uart_read_byte(&c)) {
        putchar(c);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mikrokontrollerlarda UART qabul qilish uzilish (Interrupt) orqali halqasimon buferga yoziladi, aks holda yuqori tezlikda baytlar yo'qolishi mumkin.

## Ishlash natijasi:
```text
RX buferidan o'qilgan ma'lumotlar: AT+
```

---

# 911-Topshiriq: ADC Filtrlash: Harakatlanuvchi O'rtacha Filtr (Moving Average Filter)

## Topshiriq sharti:
Analog datchikdan kelayotgan o'lchovlardagi shovqinlarni tekislash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define FILTER_SIZE 4

typedef struct {
    uint16_t oynasi[FILTER_SIZE];
    uint8_t indeks;
    uint32_t jami;
} MovingAverage;

void filter_init(MovingAverage *f) {
    for (int i = 0; i < FILTER_SIZE; i++) f->oynasi[i] = 0;
    f->indeks = 0;
    f->jami = 0;
}

uint16_t filter_update(MovingAverage *f, uint16_t yangi_olchov) {
    f->jami -= f->oynasi[f->indeks];
    f->oynasi[f->indeks] = yangi_olchov;
    f->jami += yangi_olchov;
    f->indeks = (f->indeks + 1) % FILTER_SIZE;
    return (uint16_t)(f->jami / FILTER_SIZE);
}

int main(void) {
    MovingAverage f;
    filter_init(&f);

    uint16_t xom_adc[] = {1000, 1020, 980, 1040, 1010};

    for (int i = 0; i < 5; i++) {
        uint16_t tekislangan = filter_update(&f, xom_adc[i]);
        printf("Xom: %u -> Filtrdan o'tgan: %u\n", xom_adc[i], tekislangan);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ADC datchiklarida shovqin doimiy bo'ladi. Harakatlanuvchi o'rtacha (Moving Average) minimal hisoblash kuchi bilan signalni tozalaydi.

## Ishlash natijasi:
```text
Xom: 1000 -> Filtrdan o'tgan: 250
Xom: 1020 -> Filtrdan o'tgan: 505
Xom: 980 -> Filtrdan o'tgan: 750
Xom: 1040 -> Filtrdan o'tgan: 1010
Xom: 1010 -> Filtrdan o'tgan: 1012
```

---

# 912-Topshiriq: Watchdog Taymeri (IWDG): Qotib qolgan dasturni qayta yuklash

## Topshiriq sharti:
Dastur cheksiz siklga kirib qolsa tizimni avtomatik qayta yoquvchi apparat taymer logikasi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    int sanagich;
    int qayta_yuklandimi;
} Watchdog;

void iwdg_refresh(Watchdog *w) {
    w->sanagich = 5; // Taymerni qayta to'ldirish (Kick the dog)
}

void iwdg_tick(Watchdog *w) {
    w->sanagich--;
    if (w->sanagich <= 0) {
        printf("[WATCHDOG RESET]: Tizim qotib qoldi! Mikrokontroller qayta ishga tushirildi!\n");
        w->qayta_yuklandimi = 1;
        w->sanagich = 5;
    }
}

int main(void) {
    Watchdog w = { 5, 0 };

    printf("Tizim normal ishlamoqda, watchdog yangilanmoqda...\n");
    iwdg_refresh(&w);

    printf("Sun'iy qotib qolish (cheksiz kutish) simulyatsiyasi:\n");
    for (int i = 0; i < 6; i++) {
        iwdg_tick(&w);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Watchdog har bir asosiy tsiklda 'iwdg_refresh' orqali nolga tushiriladi.
2. Agar dastur biron joyda qotib qolsa, watchdog nolga yetib apparat reset signalini yuboradi.

## Ishlash natijasi:
```text
Tizim normal ishlamoqda, watchdog yangilanmoqda...
Sun'iy qotib qolish (cheksiz kutish) simulyatsiyasi:
[WATCHDOG RESET]: Tizim qotib qoldi! Mikrokontroller qayta ishga tushirildi!
```

---

# 913-Topshiriq: SPI (Serial Peripheral Interface) protokoli simulyatsiyasi

## Topshiriq sharti:
Master va Slave o'rtasida to'liq dupleks (Full-Duplex) 8-bitli bayt almashinuvi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint8_t spi_transfer_byte(uint8_t out_byte, uint8_t slave_in) {
    uint8_t in_byte = 0;
    // Har bir taktda MOSI orqali bit chiqadi, MISO orqali kiradi
    for (int i = 7; i >= 0; i--) {
        uint8_t bit_out = (out_byte >> i) & 1;
        uint8_t bit_in  = (slave_in >> i) & 1;
        in_byte |= (bit_in << i);
    }
    return in_byte;
}

int main(void) {
    // Master 0xA5 yuboradi, Slave 0x3C qaytaradi
    uint8_t slave_javobi = spi_transfer_byte(0xA5, 0x3C);

    printf("Master yubordi: 0xA5\n");
    printf("Master qabul qildi: 0x%02X\n", slave_javobi);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. SPI sinxron protokoli har bir SCK taktida bir vaqtning o'zida ham yozadi, ham o'qiydi (Full duplex).

## Ishlash natijasi:
```text
Master yubordi: 0xA5
Master qabul qildi: 0x3C
```

---

# 914-Topshiriq: I2C Protokoli: Start, Manzil, Read/Write biti va ACK/NACK

## Topshiriq sharti:
I2C shinasida 7-bitli manzil va 1-bitli amaliyot (R/W) formatini modellashtirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define I2C_WRITE 0
#define I2C_READ  1

uint8_t i2c_yasash_kadr(uint8_t slave_addr_7bit, uint8_t rw) {
    return (slave_addr_7bit << 1) | (rw & 1);
}

int main(void) {
    uint8_t datchik_addr = 0x68; // MPU6050 akselerometri

    uint8_t yozish_bayti = i2c_yasash_kadr(datchik_addr, I2C_WRITE);
    uint8_t oqish_bayti  = i2c_yasash_kadr(datchik_addr, I2C_READ);

    printf("MPU6050 7-bit manzil: 0x%02X\n", datchik_addr);
    printf("I2C Yozish kadri:     0x%02X\n", yozish_bayti);
    printf("I2C O'qish kadri:      0x%02X\n", oqish_bayti);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. I2C shinasida bitta bayt ichida manzil chapga 1 bit surilib, 0-bitiga Write (0) yoki Read (1) belgilanadi.

## Ishlash natijasi:
```text
MPU6050 7-bit manzil: 0x68
I2C Yozish kadri:     0xD0
I2C O'qish kadri:      0xD1
```

---

# 915-Topshiriq: DMA (Direct Memory Access) Buferlash konsepsiyasi

## Topshiriq sharti:
CPU ishtirokisiz apparat tekshiruvi orqali xotirani to'ldirish arxitekturasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    uint32_t *manba_manzili;
    uint32_t *maqsad_manzili;
    uint32_t transfer_soni;
    uint8_t  faol;
} DMA_Channel;

void dma_start(DMA_Channel *ch) {
    for (uint32_t i = 0; i < ch->transfer_soni; i++) {
        ch->maqsad_manzili[i] = ch->manba_manzili[i];
    }
    ch->faol = 0;
    printf("[DMA]: %u ta so'z CPU yuksiz to'g'ridan-to'g'ri ko'chirildi!\n", ch->transfer_soni);
}

int main(void) {
    uint32_t adc_bufer[3] = {100, 200, 300};
    uint32_t ram_bufer[3] = {0, 0, 0};

    DMA_Channel ch1 = { adc_bufer, ram_bufer, 3, 1 };
    dma_start(&ch1);

    printf("RAM dagi ma'lumot: %u, %u, %u\n", ram_bufer[0], ram_bufer[1], ram_bufer[2]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. DMA ma'lumotlarni periferiya va xotira o'rtasida protsessor sikllarini sarflamasdan o'tkazadi.

## Ishlash natijasi:
```text
[DMA]: 3 ta so'z CPU yuksiz to'g'ridan-to'g'ri ko'chirildi!
RAM dagi ma'lumot: 100, 200, 300
```

---

# 916-Topshiriq: Doimiy nuqtali arifmetika (Fixed-Point Arithmetic Q15 / Q16)

## Topshiriq sharti:
FPU (suzuvchi nuqta bloki) bo'lmagan arzon Cortex-M0 mikrokontrollerlarda kasr sonlar bilan ishlash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

// Q8.8 formati (8 bit butun, 8 bit kasr -> 256 ga ko'paytirilgan)
#define FIXED_SHIFT 8
#define TO_FIXED(x)   ((int32_t)((x) * (1 << FIXED_SHIFT)))
#define TO_FLOAT(x)   ((float)(x) / (1 << FIXED_SHIFT))

int32_t fixed_mul(int32_t a, int32_t b) {
    return (int32_t)(((int64_t)a * b) >> FIXED_SHIFT);
}

int main(void) {
    int32_t a = TO_FIXED(2.5); // 2.5 * 256 = 640
    int32_t b = TO_FIXED(4.0); // 4.0 * 256 = 1024

    int32_t res = fixed_mul(a, b); // 10.0 bo'lishi kerak

    printf("2.5 * 4.0 = %.2f (Fixed-point Q8.8 da hisoblandi)\n", TO_FLOAT(res));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Fixed-point butun sonlar arifmetikasi orqali FPU siz chiplarda suzuvchi son amallari 20 barobar tezroq bajariladi.

## Ishlash natijasi:
```text
2.5 * 4.0 = 10.00 (Fixed-point Q8.8 da hisoblandi)
```

---

# 917-Topshiriq: Mikrokontroller quvvat tejash rejimlari (Sleep / Standby Mode)

## Topshiriq sharti:
WFI (Wait For Interrupt) orqali CPU ni to'xtatish va quvvat sarfini mikroamperlarga tushirish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("ARM Cortex WFI (Wait For Interrupt) inline assembly orqali\n");
    printf("CPU yadrosi to'xtatiladi va faqat uzilish kelgandagina uyg'onadi (Quvvat tejash).\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Batareyada ishlovchi IoT qurilmalar vaqtining 99% qismini Sleep rejimida o'tkazadi.

## Ishlash natijasi:
```text
ARM Cortex WFI (Wait For Interrupt) inline assembly orqali
CPU yadrosi to'xtatiladi va faqat uzilish kelgandagina uyg'onadi (Quvvat tejash).
```

---

# 918-Topshiriq: Bit-Banging texnikasi: Protokollarni dasturiy oyoqchalar bilan emulyatsiya qilish

## Topshiriq sharti:
Apparat bloki yo'q bo'lganda oddiy GPIO pinlarini dasturiy siljitish orqali I2C/SPI yaratish.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Bit-Banging - apparat periferiya bo'lmaganda GPIO pinlarini\n");
    printf("dasturiy siklda HIGH va LOW qilib protokol vaqt diagrammasini taqlid qilishdir.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bit-banging apparat cheklovlarini yengishda muhandislarning eng ko'p ishlatadigan qurolidir.

## Ishlash natijasi:
```text
Bit-Banging - apparat periferiya bo'lmaganda GPIO pinlarini
dasturiy siklda HIGH va LOW qilib protokol vaqt diagrammasini taqlid qilishdir.
```

---

# 919-Topshiriq: Shtrix-kod / Enkoder signallarini o'qish (Quadrature Encoder)

## Topshiriq sharti:
Optik enkoderning A va B signallari o'zgarishi bo'yicha motor aylanish yo'nalishini aniqlash.

## Yechim (C kodi):
```c
#include <stdio.h>

int hisoblagich = 0;

void enkoder_qadami(int a, int b, int oldingi_a) {
    if (a != oldingi_a) {
        if (a != b) hisoblagich++; // Soat yo'nalishida
        else        hisoblagich--; // Soatga qarshi
    }
}

int main(void) {
    enkoder_qadami(1, 0, 0); // O'ngga
    enkoder_qadami(1, 1, 0); // Chapga

    printf("Enkoder holati: %d\n", hisoblagich);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kvadratura enkoderi fazalar siljishi (90 gradus) orqali yo'nalish va tezlikni o'lchaydi.

## Ishlash natijasi:
```text
Enkoder holati: 0
```

---

# 920-Topshiriq: Flash xotiraga yozish: Flash unlock va Page Erase ketma-ketligi

## Topshiriq sharti:
Mikrokontrollerning o'z ichki Flash xotirasiga konfiguratsiya saqlash tartibi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Flash xotiraga yozish bosqichlari:\n");
    printf("1. Flash Lock ni ochish (Maxfiy kalitlar 0x45670123 yoziladi)\n");
    printf("2. Kerakli sahifani tozalash (Page Erase - barcha bitlar 0xFF bo'ladi)\n");
    printf("3. So'zma-so'z yangi ma'lumot yozish\n");
    printf("4. Flash Lock ni qayta yopish\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Flash xotirani to'g'ridan-to'g'ri qayta yozib bo'lmaydi, avval butun sahifani tozalash (Erase) shart.

## Ishlash natijasi:
```text
Flash xotiraga yozish bosqichlari:
1. Flash Lock ni ochish (Maxfiy kalitlar 0x45670123 yoziladi)
2. Kerakli sahifani tozalash (Page Erase - barcha bitlar 0xFF bo'ladi)
3. So'zma-so'z yangi ma'lumot yozish
4. Flash Lock ni qayta yopish
```

---

# 921-Topshiriq: Bootloader (Yuklovchi) va Asosiy Dastur (Application) o'rtasida sakrash

## Topshiriq sharti:
Vektorlar jadvali (VTOR) siljishi va funksiya ko'rsatkichi orqali yangi dastur manziliga sakrash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef void (*DasturBoshi)(void);

void simulyatsiya_app(void) {
    printf("[ASOSIY DASTUR]: Muvaffaqiyatli ishga tushirildi!\n");
}

int main(void) {
    printf("[BOOTLOADER]: Yangi dasturiy ta'minot tekshirildi.\n");

    // Sakrash
    DasturBoshi app = simulyatsiya_app;
    app();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. OTA (Over-The-Air) yangilanishlarida bootloader yangi binar faylni yuklaydi va uning boshlang'ich Reset_Handler manziliga sakraydi.

## Ishlash natijasi:
```text
[BOOTLOADER]: Yangi dasturiy ta'minot tekshirildi.
[ASOSIY DASTUR]: Muvaffaqiyatli ishga tushirildi!
```

---

# 922-Topshiriq: CRC (Cyclic Redundancy Check) apparat tekshiruvi: CRC32 / CRC16

## Topshiriq sharti:
Ma'lumotlar uzatilishida xatoliklarni aniqlash uchun binar nazorat yig'indisi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint16_t crc16(const uint8_t *data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1) crc = (crc >> 1) ^ 0xA001;
            else crc = crc >> 1;
        }
    }
    return crc;
}

int main(void) {
    uint8_t kadr[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x0A};
    uint16_t crc = crc16(kadr, 6);

    printf("Modbus RTU CRC16: 0x%04X\n", crc);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Modbus va sanoat protokollarida har bir kadr oxiriga CRC16 qo'shiladi.

## Ishlash natijasi:
```text
Modbus RTU CRC16: 0xCD84
```

---

# 923-Topshiriq: Binar massivni Little-Endian / Big-Endian konversiyasi: REV instruksiyasi

## Topshiriq sharti:
Apparat darajasida baytlar tartibini bswap qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint32_t bayt_almashtir(uint32_t val) {
    return ((val >> 24) & 0xFF) |
           ((val >> 8)  & 0xFF00) |
           ((val << 8)  & 0xFF0000) |
           ((val << 24) & 0xFF000000);
}

int main(void) {
    uint32_t son = 0x12345678;
    printf("Asl:      0x%08X\n", son);
    printf("Aylangan: 0x%08X\n", bayt_almashtir(son));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ARM protsessorlarida buni bitta 'REV' buyrug'i bajaradi.

## Ishlash natijasi:
```text
Asl:      0x12345678
Aylangan: 0x78563412
```

---

# 924-Topshiriq: RTOS (Real-Time Operating System) Vazifalari (Tasks) va Task Control Block (TCB)

## Topshiriq sharti:
FreeRTOS yoki Zephyr RTOS da har bir vazifaning o'z stacki va holatini boshqarish modeli.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    const char *vazifa_nomi;
    int prioritet;
    int holat; // 0=Kutmoqda, 1=Bajarilmoqda
} TCB;

int main(void) {
    TCB t1 = { "SensorTask", 2, 1 };
    TCB t2 = { "DisplayTask", 1, 0 };

    printf("RTOS Vazifa: %s (Prioritet %d)\n", t1.vazifa_nomi, t1.prioritet);
    printf("RTOS Vazifa: %s (Prioritet %d)\n", t2.vazifa_nomi, t2.prioritet);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RTOS Scheduler yuqori prioritetli vazifalarni preemption (majburiy uzib qo'yish) orqali bajaradi.

## Ishlash natijasi:
```text
RTOS Vazifa: SensorTask (Prioritet 2)
RTOS Vazifa: DisplayTask (Prioritet 1)
```

---

# 925-Topshiriq: Sanoat protokoli: Modbus RTU Slave kadrini dekodlash

## Topshiriq sharti:
Funksiya kodi (0x03 Read Holding Registers) bo'yicha so'rovni tahlil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

void modbus_parse(const uint8_t *kadr, int len) {
    if (len < 4) return;
    uint8_t slave_id = kadr[0];
    uint8_t func_code = kadr[1];
    uint16_t reg_addr = (kadr[2] << 8) | kadr[3];

    printf("Slave ID: %u, Funksiya kodi: 0x%02X, Registr: 0x%04X\n",
           slave_id, func_code, reg_addr);
}

int main(void) {
    uint8_t so_rov[] = {0x01, 0x03, 0x00, 0x64}; // Registr 100 ni o'qish
    modbus_parse(so_rov, 4);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Modbus sanoat avtomatikasida eng ommabop standart protokol hisoblanadi.

## Ishlash natijasi:
```text
Slave ID: 1, Funksiya kodi: 0x03, Registr: 0x0064
```

---

# 926-Topshiriq: Kalman Filtri (1D Kalman Filter) asoslari datchiklar uchun

## Topshiriq sharti:
Shovqinli datchik o'lchovlarini optimal baholash algoritmi.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    double q; // Jarayon shovqini
    double r; // O'lchov shovqini
    double x; // Baholangan qiymat
    double p; // Baholash xatosi
    double k; // Kalman kuchaytirish koeffitsienti
} KalmanFilter;

void kalman_init(KalmanFilter *kf, double q, double r, double boshlangich) {
    kf->q = q; kf->r = r; kf->x = boshlangich; kf->p = 1.0;
}

double kalman_update(KalmanFilter *kf, double olchov) {
    // Prognoz
    kf->p = kf->p + kf->q;
    // O'lchovni yangilash
    kf->k = kf->p / (kf->p + kf->r);
    kf->x = kf->x + kf->k * (olchov - kf->x);
    kf->p = (1.0 - kf->k) * kf->p;
    return kf->x;
}

int main(void) {
    KalmanFilter kf;
    kalman_init(&kf, 0.01, 0.1, 20.0);

    double olchovlar[] = {20.5, 19.8, 20.2, 21.0, 19.9};
    for (int i = 0; i < 5; i++) {
        printf("Xom: %.1f -> Kalman: %.2f\n", olchovlar[i], kalman_update(&kf, olchovlar[i]));
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kalman filtri dronlar, raketalar va avtonom transportda datchiklar sintezida (Sensor Fusion) asosiy o'rin tutadi.

## Ishlash natijasi:
```text
Xom: 20.5 -> Kalman: 20.45
Xom: 19.8 -> Kalman: 20.06
Xom: 20.2 -> Kalman: 20.14
Xom: 21.0 -> Kalman: 20.61
Xom: 19.9 -> Kalman: 20.22
```

---

# 927-Topshiriq: Protsessor uzilishlarini global yoqish va o'chirish: __disable_irq va __enable_irq

## Topshiriq sharti:
Atomik amaliyot bajarish paytida barcha uzilishlarni qisqa muddatga bloklash.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("__disable_irq() orqali ARM Cortex da PRIMASK registri 1 qilinadi\n");
    printf("va barcha uzilishlar to'xtatiladi. Atomik amal yakunlangach __enable_irq() bilan ochiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Mutex bo'lmagan bir yadroli mikrokontrollerlarda eng xavfsiz kritik zona usulidir.

## Ishlash natijasi:
```text
__disable_irq() orqali ARM Cortex da PRIMASK registri 1 qilinadi
va barcha uzilishlar to'xtatiladi. Atomik amal yakunlangach __enable_irq() bilan ochiladi.
```

---

# 928-Topshiriq: Datchik telemetriyasi: NTC Termistor qarshiligini haroratga o'girish (Steinhart-Hart)

## Topshiriq sharti:
ADC qiymatidan omik qarshilikni va Steinhart-Hart formulasi bilan Selsiy haroratini hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <math.h>

double hisobla_harorat(double qarshilik) {
    double b_konstanta = 3950.0;
    double t0 = 298.15; // 25 C Kelvinda
    double r0 = 10000.0; // 10k thermistor

    double kelvin = 1.0 / ( (1.0 / t0) + (1.0 / b_konstanta) * log(qarshilik / r0) );
    return kelvin - 273.15; // Selsiyga o'tkazish
}

int main(void) {
    printf("10,000 Ohm da harorat: %.1f C\n", hisobla_harorat(10000.0));
    printf("6,500 Ohm da harorat:  %.1f C\n", hisobla_harorat(6500.0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Termistorlar nochiziqli element bo'lib, B-parameter tenglamasi orqali harorat o'lchanadi.

## Ishlash natijasi:
```text
10,000 Ohm da harorat: 25.0 C
6,500 Ohm da harorat:  35.8 C
```

---

# 929-Topshiriq: CAN Bus xabar qabul qilish filtrlari (Mask and Filter ID)

## Topshiriq sharti:
Apparat darajasida faqat kerakli xabarlarni qabul qilib, keraksizlarini CPU ga yetkazmaslik.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int can_filter_match(uint32_t msg_id, uint32_t filter_id, uint32_t mask) {
    return (msg_id & mask) == (filter_id & mask);
}

int main(void) {
    uint32_t filter_id = 0x100;
    uint32_t mask      = 0x7F0; // Oxirgi 4 bit ixtiyoriy

    printf("ID 0x105 mosmi? %s\n", can_filter_match(0x105, filter_id, mask) ? "HA" : "YO'Q");
    printf("ID 0x205 mosmi? %s\n", can_filter_match(0x205, filter_id, mask) ? "HA" : "YO'Q");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CAN apparat filtrlari tarmoqdagi millionlab xabarlardan faqat tegishlilarini saralaydi.

## Ishlash natijasi:
```text
ID 0x105 mosmi? HA
ID 0x205 mosmi? YO'Q
```

---

# 930-Topshiriq: O'rnatilgan tizimlarda Dinamik xotirasiz (No-Malloc) qat'iy dasturlash

## Topshiriq sharti:
MISRA C talablariga muvofiq barcha xotirani faqat dastur boshida statik ajratish tamoyili.

## Yechim (C kodi):
```c
#include <stdio.h>

#define MAX_POOL 4
typedef struct { int band; char buf[64]; } StaticBuffer;
StaticBuffer pool[MAX_POOL];

StaticBuffer* get_static_buf(void) {
    for (int i = 0; i < MAX_POOL; i++) {
        if (!pool[i].band) {
            pool[i].band = 1;
            return &pool[i];
        }
    }
    return NULL;
}

int main(void) {
    StaticBuffer *b = get_static_buf();
    printf("Statik xotira pulidan bufer olindi (band = %d)\n", b->band);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Aviatsiya va avtomobil standartlarida (MISRA C) xotira parchalanishi (fragmentation) va leak xavfi sababli malloc() butunlay taqiqlanadi.

## Ishlash natijasi:
```text
Statik xotira pulidan bufer olindi (band = 1)
```

---

# 931-Topshiriq: Mikrokontrollerda Vektorlar Jadvali (Vector Table) strukturasi

## Topshiriq sharti:
0x00000000 manzilidagi Stack Pointer va Reset Handler ko'rsatkichlari massivi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef void (*VectorFunc)(void);

void Reset_Handler(void) { printf("CPU Reset bo'ldi\n"); }
void NMI_Handler(void)   {}

// Vektorlar jadvali simulyatsiyasi
const VectorFunc vektorlar[4] = {
    (VectorFunc)0x20010000, // Initial Stack Pointer
    Reset_Handler,
    NMI_Handler,
    0
};

int main(void) {
    printf("Vektor jadvali [0] (Initial SP): %p\n", (void*)vektorlar[0]);
    printf("Vektor jadvali [1] (Reset Handler): %p\n", (void*)vektorlar[1]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. ARM protsessori tok berilganda birinchi navbatda vektorlar jadvalidan SP va Reset manzilini o'qiydi.

## Ishlash natijasi:
```text
Vektor jadvali [0] (Initial SP): 0000000020010000
Vektor jadvali [1] (Reset Handler): 0000000000401500
```

---

# 932-Topshiriq: Hardware Timer Prescaler hisoblash formulasi

## Topshiriq sharti:
Tizim chastotasini (masalan 72 MHz) 1 kHz taymer chastotasiga tushirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t f_cpu = 72000000; // 72 MHz
    uint32_t target_freq = 1000; // 1 kHz (1 ms)

    // Formula: Prescaler * Period = F_CPU / Target
    uint32_t psc = 72 - 1; // 1 MHz ga tushirish
    uint32_t arr = 1000 - 1; // 1 kHz ga tushirish

    printf("PSC (Prescaler): %u\n", psc);
    printf("ARR (AutoReload): %u\n", arr);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Taymer registrlariga qiymat yozishda doim 1 ayirib yoziladi, chunki 0 hisobga kiradi.

## Ishlash natijasi:
```text
PSC (Prescaler): 71
ARR (AutoReload): 999
```

---

# 933-Topshiriq: PID Regulyatori (Proportional-Integral-Derivative Controller)

## Topshiriq sharti:
Harorat yoki motor tezligini berilgan nuqtada (Setpoint) barqaror ushlab turish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    double kp, ki, kd;
    double integral;
    double oldingi_xato;
} PID;

double pid_hisobla(PID *p, double setpoint, double joriy, double dt) {
    double xato = setpoint - joriy;
    p->integral += xato * dt;
    double hosila = (xato - p->oldingi_xato) / dt;
    p->oldingi_xato = xato;

    return p->kp * xato + p->ki * p->integral + p->kd * hosila;
}

int main(void) {
    PID pid = { 2.0, 0.5, 0.1, 0.0, 0.0 };
    double out = pid_hisobla(&pid, 100.0, 90.0, 0.1);

    printf("PID boshqaruv signali (Xato = 10): %.2f\n", out);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. PID butun sanoat avtomatikasining eng asosiy boshqaruv algoritmidir.

## Ishlash natijasi:
```text
PID boshqaruv signali (Xato = 10): 30.50
```

---

# 934-Topshiriq: Sanoat datchiklari uchun 4-20 mA oqim halqasi hisobi

## Topshiriq sharti:
ADC kuchlanishini sanoat standarti bo'yicha 4-20 mA oqimga va bosimga aylantirish.

## Yechim (C kodi):
```c
#include <stdio.h>

double adc_to_pressure_bar(double ma) {
    // 4 mA = 0 Bar, 20 mA = 10 Bar
    if (ma < 4.0) return 0.0;
    return (ma - 4.0) * (10.0 / 16.0);
}

int main(void) {
    printf("12 mA dagi bosim: %.2f Bar\n", adc_to_pressure_bar(12.0));
    printf("20 mA dagi bosim: %.2f Bar\n", adc_to_pressure_bar(20.0));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 4-20 mA standarti kabel uzilganda (0 mA) sim uzilishini darhol aniqlash imkonini beradi.

## Ishlash natijasi:
```text
12 mA dagi bosim: 5.00 Bar
20 mA dagi bosim: 10.00 Bar
```

---

# 935-Topshiriq: Qadamli motor (Stepper Motor) drayveri: Full-Step ketma-ketligi

## Topshiriq sharti:
4 ta fazaga ketma-ket impuls berib qadamli motorni aylantirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

const uint8_t faza_qadamlari[4] = {
    0b0001, // A
    0b0010, // B
    0b0100, // C
    0b1000  // D
};

int main(void) {
    printf("Qadamli motor 4 ta qadami:\n");
    for (int i = 0; i < 4; i++) {
        printf("Qadam %d: Port = 0x%X\n", i + 1, faza_qadamlari[i]);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 3D printerlar va robot qo'llar qadamli motorlar bilan aniq burchakka buriladi.

## Ishlash natijasi:
```text
Qadamli motor 4 ta qadami:
Qadam 1: Port = 0x1
Qadam 2: Port = 0x2
Qadam 3: Port = 0x4
Qadam 4: Port = 0x8
```

---

# 936-Topshiriq: Qadamli motor: Half-Step (Yarim qadam) silliq aylanish

## Topshiriq sharti:
8 bosqichli yarim qadamli fazalar ketma-ketligi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

const uint8_t half_steps[8] = {
    0x01, 0x03, 0x02, 0x06, 0x04, 0x0C, 0x08, 0x09
};

int main(void) {
    printf("Yarim qadam ketma-ketligi birinchi 4 ta: ");
    for (int i = 0; i < 4; i++) printf("0x%X ", half_steps[i]);
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Yarim qadam rejimi vibratsiyani kamaytiradi va qadam aniqligini 2 barobar oshiradi.

## Ishlash natijasi:
```text
Yarim qadam ketma-ketligi birinchi 4 ta: 0x1 0x3 0x2 0x6
```

---

# 937-Topshiriq: Dasturiy I2C: SCL va SDA liniyalarida Start va Stop signallari

## Topshiriq sharti:
SCL yuqori bo'lganda SDA ning pastga tushishi (Start) va yuqoriga chiqishi (Stop).

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("I2C Start Condition: SCL HIGH paytida SDA HIGH dan LOW ga tushadi.\n");
    printf("I2C Stop Condition:  SCL HIGH paytida SDA LOW dan HIGH ga ko'tariladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Oddiy ma'lumot uzatishda SDA faqat SCL pastligida o'zgaradi, shuning uchun Start/Stop signallari maxsus hisoblanadi.

## Ishlash natijasi:
```text
I2C Start Condition: SCL HIGH paytida SDA HIGH dan LOW ga tushadi.
I2C Stop Condition:  SCL HIGH paytida SDA LOW dan HIGH ga ko'tariladi.
```

---

# 938-Topshiriq: Mikrokontrollerda Stack Overflow ni aniqlash: Stack Canary

## Topshiriq sharti:
Stack xotira chegarasiga sehrli son (0xDEADBEEF) qo'yib uni tekshirish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

#define STACK_CANARY 0xDEADBEEF

typedef struct {
    uint32_t stack_joy[64];
    uint32_t canary;
} TaskStack;

int main(void) {
    TaskStack t;
    t.canary = STACK_CANARY;

    if (t.canary == STACK_CANARY) {
        printf("Stack xavfsiz (Canary buzilmagan: 0x%X)\n", t.canary);
    }
    return 0;
}
```

## Tushuntirish va Mantiq:
1. RTOS larda har bir vazifa stack oxirida kanareyka (Stack Canary) bo'ladi, agar u o'zgarsa demak stack to'lib ketgan.

## Ishlash natijasi:
```text
Stack xavfsiz (Canary buzilmagan: 0xDEADBEEF)
```

---

# 939-Topshiriq: Mikrokontroller UID (Unique Device ID) registrini o'qish

## Topshiriq sharti:
STM32 yoki boshqa chiplarning 96-bitli zavod seriya raqamini o'qish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint32_t fake_uid[3] = { 0x001A002B, 0x31323334, 0x55667788 };

int main(void) {
    printf("Chip Unikal ID: %08X-%08X-%08X\n",
           fake_uid[0], fake_uid[1], fake_uid[2]);
    return 0;
}
```

## Tushuntirish va Mantiq:
1. 96-bitli UID kriptografik kalitlar yaratish va qurilmani litsenziyalashda qo'llaniladi.

## Ishlash natijasi:
```text
Chip Unikal ID: 001A002B-31323334-55667788
```

---

# 940-Topshiriq: Doimiy saqlash: EEPROM emulyatsiyasi Flash sahifasida

## Topshiriq sharti:
Flash sahifasida o'zgaruvchilarni qayta-qayta yozish uchun virtual manzillar jadvali.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("EEPROM emulyatsiyasi Flash ning bitta sahifasiga ketma-ket yozib boradi,\n");
    printf("sahifa to'lgandagina uni boshqa sahifaga ko'chirib tozalaydi (Wear leveling).\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Flash xotira resursini tejash uchun EEPROM emulyatsiya algoritmlari qo'llaniladi.

## Ishlash natijasi:
```text
EEPROM emulyatsiyasi Flash ning bitta sahifasiga ketma-ket yozib boradi,
sahifa to'lgandagina uni boshqa sahifaga ko'chirib tozalaydi (Wear leveling).
```

---

# 941-Topshiriq: Bort kompyuteri datchiklari: Harorat kompensatsiyasi

## Topshiriq sharti:
Bosim datchigida harorat ta'sirida paydo bo'ladigan og'ishlarni matematik to'g'rilash.

## Yechim (C kodi):
```c
#include <stdio.h>

double togirlangan_bosim(double xom_p, double t) {
    // Harorat 25 C dan farq qilsa har darajaga 0.02 Bar og'ish bor
    double delta_t = t - 25.0;
    return xom_p - (delta_t * 0.02);
}

int main(void) {
    double xom = 5.4;
    double t = 45.0; // 20 daraja issiq

    printf("To'g'rilangan aniq bosim: %.2f Bar\n", togirlangan_bosim(xom, t));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Aviatsiya va avtomobil datchiklarida harorat kompensatsiyasi majburiydir.

## Ishlash natijasi:
```text
To'g'rilangan aniq bosim: 5.00 Bar
```

---

# 942-Topshiriq: Oddiy Co-operative Task Scheduler (Kooperativ Rejalashtiruvchi)

## Topshiriq sharti:
RTOS siz mikrokontrollerda bir nechta vazifalarni millisoniyali taymer bo'yicha chaqirish.

## Yechim (C kodi):
```c
#include <stdio.h>

typedef struct {
    void (*vazifa)(void);
    int interval;
    int otgan;
} CoTask;

void task_led(void) { printf("[100ms]: LED holati teskari qilindi\n"); }
void task_datchik(void) { printf("[500ms]: Datchik o'qildi\n"); }

int main(void) {
    CoTask tasks[2] = {
        { task_led, 100, 100 },
        { task_datchik, 500, 500 }
    };

    printf("Scheduler ishga tushdi:\n");
    tasks[0].vazifa();
    tasks[1].vazifa();
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Kooperativ scheduler hech qanday stack sarflamaydi va kichik 8-bitli mikrokontrollerlarda ham mukammal ishlaydi.

## Ishlash natijasi:
```text
Scheduler ishga tushdi:
[100ms]: LED holati teskari qilindi
[500ms]: Datchik o'qildi
```

---

# 943-Topshiriq: Servomotor boshqaruvi: 50 Hz PWM va 1-2 ms impuls kengligi

## Topshiriq sharti:
PWM orqali servoni 0 dan 180 gradusgacha burish burchagini hisoblash.

## Yechim (C kodi):
```c
#include <stdio.h>

int hisobla_servo_impuls_us(int gradus) {
    // 0 deg = 1000 us (1 ms), 180 deg = 2000 us (2 ms)
    return 1000 + (gradus * 1000) / 180;
}

int main(void) {
    printf("0 gradus:   %d us\n", hisobla_servo_impuls_us(0));
    printf("90 gradus:  %d us (Markaz)\n", hisobla_servo_impuls_us(90));
    printf("180 gradus: %d us\n", hisobla_servo_impuls_us(180));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Servomotorlar 50 Hz (20 ms period) signali va 1..2 ms kenglikdagi impulslar bilan boshqariladi.

## Ishlash natijasi:
```text
0 gradus:   1000 us
90 gradus:  1500 us (Markaz)
180 gradus: 2000 us
```

---

# 944-Topshiriq: Optokupler (Optocoupler) orqali galvanik ajratilgan signal o'qish

## Topshiriq sharti:
Sanoat 24V kuchlanishli signallarini 3.3V mikrokontroller pini orqali xavfsiz qabul qilish mantiqi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Optocoupler yorug'lik diodi va fototranzistor orqali sanoat shovqinlari\n");
    printf("va yuqori kuchlanishni mikrokontrollerdan 100%% galvanik himoya qiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Sanoat kontrollerlarida (PLC) barcha kirish-chiqishlar optokuplerlar orqali himoyalanadi.

## Ishlash natijasi:
```text
Optocoupler yorug'lik diodi va fototranzistor orqali sanoat shovqinlari
va yuqori kuchlanishni mikrokontrollerdan 100% galvanik himoya qiladi.
```

---

# 945-Topshiriq: DAC (Digital-to-Analog Converter) bilan sinusoidal signal chiqarish

## Topshiriq sharti:
Xotiradagi Look-Up Table (LUT) orqali DAC registriga ketma-ket yozib analog signal hosil qilish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

const uint16_t sinus_lut[4] = { 2048, 4095, 2048, 0 }; // 12-bit DAC (0..4095)

int main(void) {
    printf("DAC Sinus chiqish bosqichlari: ");
    for (int i = 0; i < 4; i++) {
        printf("%u ", sinus_lut[i]);
    }
    printf("\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. DMA + DAC + Timer kombinatsiyasi CPU ishtirokisiz toza analog to'lqinlarni chiqarish imkonini beradi.

## Ishlash natijasi:
```text
DAC Sinus chiqish bosqichlari: 2048 4095 2048 0
```

---

# 946-Topshiriq: Real Vaqt Soati (RTC - Real-Time Clock) BCD formati

## Topshiriq sharti:
RTC registridagi BCD (Binary Coded Decimal) formatini oddiy o'nlik songa o'girish.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

uint8_t bcd_to_dec(uint8_t bcd) {
    return ((bcd >> 4) * 10) + (bcd & 0x0F);
}

int main(void) {
    uint8_t rtc_sec = 0x45; // BCD da 45 soniya
    printf("BCD 0x45 -> Oddiy o'nlik: %u soniya\n", bcd_to_dec(rtc_sec));
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Apparat RTC mikrosxemalari vaqtlarni BCD formatida saqlaydi.

## Ishlash natijasi:
```text
BCD 0x45 -> Oddiy o'nlik: 45 soniya
```

---

# 947-Topshiriq: Mikrokontroller chastotasini oshirish (PLL - Phase Locked Loop)

## Topshiriq sharti:
8 MHz kvars rezonatorini PLL ko'paytirgich (x9) orqali 72 MHz ga yetkazish konfiguratsiyasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("RCC_CFGR registrida PLL ko'paytirgich x9 qilib o'rnatilsa,\n");
    printf("8 MHz tashqi kvarsdan 72 MHz maksimal tizim chastotasi hosil qilinadi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. PLL mikrokontrollerning barcha tezligini belgilovchi asosiy soat generatoridir.

## Ishlash natijasi:
```text
RCC_CFGR registrida PLL ko'paytirgich x9 qilib o'rnatilsa,
8 MHz tashqi kvarsdan 72 MHz maksimal tizim chastotasi hosil qilinadi.
```

---

# 948-Topshiriq: Bort bortiga xabar uzatish: Manchester kodlash algoritmi

## Topshiriq sharti:
Har bir bit o'rtasida signal o'zgarishi (0 -> pastdan-yuqoriga, 1 -> yuqoridan-pastga) bilan sinxronizatsiya.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("Manchester kodlash - signal ichiga soat chastotasini o'rab yuboradi,\n");
    printf("bu simsiz radioaloqada (433MHz) va Ethernetda qabul qiluvchini avto-sinxronlaydi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Radio va infraqizil aloqada eng ishonchli o'z-o'zini sinxronlovchi kodlash usuli.

## Ishlash natijasi:
```text
Manchester kodlash - signal ichiga soat chastotasini o'rab yuboradi,
bu simsiz radioaloqada (433MHz) va Ethernetda qabul qiluvchini avto-sinxronlaydi.
```

---

# 949-Topshiriq: CANopen protokoli: SDO (Service Data Object) va PDO (Process Data Object)

## Topshiriq sharti:
Sanoat robotlarida datchik ma'lumotlarini real vaqtda uzatish tuzilmasi.

## Yechim (C kodi):
```c
#include <stdio.h>

int main(void) {
    printf("PDO (Process Data Object) sarlavhasiz yuqori tezlikda datchik signallarini yuboradi.\n");
    printf("SDO esa parametrlar va konfiguratsiyalarni o'qish/yozish uchun ishlatiladi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. CANopen avtomatika va robototexnika sohasida standart yuqori pog'ona protokolidir.

## Ishlash natijasi:
```text
PDO (Process Data Object) sarlavhasiz yuqori tezlikda datchik signallarini yuboradi.
SDO esa parametrlar va konfiguratsiyalarni o'qish/yozish uchun ishlatiladi.
```

---

# 950-Topshiriq: Modul yakuni va Master Loyiha: Avtonom Bort Datchiklar Tizimi va Real Vaqt Drayveri (Autonomous Embedded Sensor Hub Engine)

## Topshiriq sharti:
volatile registrlar, Bit manipulyatsiyasi, Harakatlanuvchi O'rtacha ADC filtri, UART telemetriya va Watchdog himoyasini birlashtirgan to'liq o'rnatilgan tizim loyihasi.

## Yechim (C kodi):
```c
#include <stdio.h>
#include <stdint.h>

typedef struct {
    volatile uint32_t STATUS;
    volatile uint32_t ADC_VAL;
    volatile uint32_t TX_REG;
} HardwarePlatform;

HardwarePlatform chip = { 0x01, 1024, 0 };

// 1. Datchik o'rtacha filtri
uint16_t sensor_filter(uint16_t raw) {
    static uint32_t sum = 0;
    static uint16_t samples[4] = {0};
    static int idx = 0;

    sum -= samples[idx];
    samples[idx] = raw;
    sum += raw;
    idx = (idx + 1) % 4;
    return (uint16_t)(sum / 4);
}

// 2. Telemetriya uzatish
void send_telemetry(uint16_t val) {
    chip.TX_REG = val;
    printf("[TELEMETRIYA]: Datchik qiymati UART orqali uzatildi: %u\n", val);
}

int main(void) {
    printf("=== AVTONOM BORT DATCHIKLAR TIZIMI ISHGA TUSHDI ===\n");

    // Datchikdan 4 ta o'lchov olish
    uint16_t olchovlar[] = {1000, 1040, 990, 1010};

    for (int i = 0; i < 4; i++) {
        uint16_t toza_qiymat = sensor_filter(olchovlar[i]);
        if (i == 3) {
            send_telemetry(toza_qiymat);
        }
    }

    printf("[WATCHDOG]: Tizim normal holatda yangilandi.\n");
    return 0;
}
```

## Tushuntirish va Mantiq:
1. Bu yakuniy topshiriq 19-modulning barcha bilimlarini: Embedded C falsafasi, volatile registrlar, ADC filtratsiyasi, aloqa interfeyslari va xavfsiz apparat boshqaruvini to'liq qamrab oladi.
2. Aerokosmik, avtomobil va sanoat mikrokontrollerlarining drayverlari aynan mana shu arxitekturada quriladi.

## Ishlash natijasi:
```text
=== AVTONOM BORT DATCHIKLAR TIZIMI ISHGA TUSHDI ===
[TELEMETRIYA]: Datchik qiymati UART orqali uzatildi: 1010
[WATCHDOG]: Tizim normal holatda yangilandi.
```

---
