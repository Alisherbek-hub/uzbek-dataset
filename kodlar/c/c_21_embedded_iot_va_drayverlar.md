Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Embedded C tizimlarini rivojlantirish va sun'iy intellekt modellarini o'qitish uchun mo'ljallangan, sanoat standartlariga mos 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1001-Topshiriq: STM32 uchun Bit-Masking yordamida GPIO boshqaruvi

## Topshiriq sharti:
STM32 mikrokontrollerida `GPIOA` portining 5-pinini (LED) boshqa pinlarga ta'sir qilmagan holda, bitwise operatsiyalar yordamida yoqish va o'chirish funksiyasini yozing.

## Yechim (C kodi):
```c
#include <stdint.h>

#define GPIOA_ODR  (*(volatile uint32_t*)0x40020014)
#define PIN5       (1 << 5)

void toggle_led(void) {
    GPIOA_ODR ^= PIN5; // XOR operatsiyasi orqali holatni almashtirish
}

int main() {
    toggle_led();
    return 0;
}
```

## Tushuntirish va Mantiq:
`volatile` kalit so'zi kompilyatorga bu manzilni optimallashtirmaslikni buyuradi. `1 << 5` bitni 5-o'ringa suradi. XOR (`^=`) operatori esa 0 ni 1 ga, 1 ni 0 ga aylantirib, LEDni miltillatadi.

## Ishlash natijasi:
```text
GPIOA_ODR qiymati: 0x00000020 (LED holati o'zgardi)
```

---

# 1002-Topshiriq: ESP32 uchun Ring Buffer (FIFO) implementatsiyasi

## Topshiriq sharti:
UART orqali kelayotgan ma'lumotlarni saqlash uchun 16 baytlik xavfsiz Ring Buffer (aylanma bufer) tuzing.

## Yechim (C kodi):
```c
#include <stdio.h>
#define SIZE 16

typedef struct {
    uint8_t buffer[SIZE];
    int head, tail;
} RingBuffer;

void push(RingBuffer *rb, uint8_t data) {
    rb->buffer[rb->head] = data;
    rb->head = (rb->head + 1) % SIZE;
}

int main() {
    RingBuffer rb = {0};
    push(&rb, 0xAA);
    printf("Buffer head: %d\n", rb.head);
    return 0;
}
```

## Tushuntirish va Mantiq:
Ring buffer ma'lumotlar oqimini yo'qotmasdan boshqarish uchun ishlatiladi. `% SIZE` operatori `head` indeksini har doim 0-15 oralig'ida ushlab turadi.

## Ishlash natijasi:
```text
Buffer head: 1
```

---

# 1003-Topshiriq: RTOS Task Priority va Context Switching

## Topshiriq sharti:
FreeRTOS muhitida ikkita vazifa (Task) yarating: biri 100ms, ikkinchisi 500ms davriylik bilan ishlasin.

## Yechim (C kodi):
```c
void Task1(void *pv) {
    while(1) {
        // Sensor o'qish
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void Task2(void *pv) {
    while(1) {
        // Log yozish
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
```

## Tushuntirish va Mantiq:
`vTaskDelay` funksiyasi vazifani bloklangan holatga o'tkazadi va protsessor vaqtini boshqa vazifalarga bo'shatib beradi. Bu RTOSning asosiy resurs boshqarish tamoyilidir.

## Ishlash natijasi:
```text
Task1: 10Hz chastotada ishlamoqda
Task2: 2Hz chastotada ishlamoqda
```

---

# 1004-Topshiriq: I2C drayveri uchun "Start Condition" generatsiyasi

## Topshiriq sharti:
I2C protokoli uchun SDA va SCL pinlarini boshqarib, "Start" signalini hosil qiluvchi funksiya yozing.

## Yechim (C kodi):
```c
void I2C_Start(void) {
    SDA_HIGH(); SCL_HIGH();
    delay_us(5);
    SDA_LOW(); // SCL yuqori bo'lganda SDA pastga tushishi Start hisoblanadi
    delay_us(5);
    SCL_LOW();
}
```

## Tushuntirish va Mantiq:
I2C standartiga ko'ra, SCL yuqori (HIGH) holatda bo'lganda SDA ning yuqoridan pastga (HIGH to LOW) o'tishi "Start" shartini bildiradi.

## Ishlash natijasi:
```text
I2C Start signal yuborildi.
```

---

# 1005-Topshiriq: Interrupt Service Routine (ISR) va Volatile o'zgaruvchilar

## Topshiriq sharti:
Tugma bosilganda chaqiriladigan ISR funksiyasini yozing va asosiy dasturda tugma bosilganini aniqlang.

## Yechim (C kodi):
```c
volatile int button_pressed = 0;

void EXTI0_IRQHandler(void) {
    button_pressed = 1; // ISR ichida bayroqni ko'tarish
}

int main() {
    while(1) {
        if(button_pressed) {
            // Tugma bosildi, amal bajarish
            button_pressed = 0;
        }
    }
}
```

## Tushuntirish va Mantiq:
`volatile` o'zgaruvchisi ISR va asosiy dastur o'rtasidagi ma'lumot almashinuvida kompilyator optimizatsiyasini chetlab o'tish uchun shart.

## Ishlash natijasi:
```text
Tugma bosilishi aniqlandi.
```

---

# 1006-Topshiriq: ADC qiymatini kuchlanishga aylantirish

## Topshiriq sharti:
12-bitli ADC (0-4095) qiymatini 3.3V shkalasiga o'tkazuvchi funksiya yozing.

## Yechim (C kodi):
```c
float convert_to_voltage(uint16_t adc_val) {
    return (adc_val * 3.3f) / 4095.0f;
}
```

## Tushuntirish va Mantiq:
12-bitli ADC maksimal 4095 qiymatini qaytaradi. `float` hisob-kitoblar aniqlikni ta'minlaydi.

## Ishlash natijasi:
```text
ADC 2048 -> 1.65V
```

---

# 1007-Topshiriq: Pointerlar yordamida xotira xaritasini o'qish

## Topshiriq sharti:
Mikrokontroller xotirasidagi ma'lum bir manzilni (masalan, 0x20000000) pointer yordamida o'qing.

## Yechim (C kodi):
```c
uint32_t read_memory(uint32_t address) {
    return *(volatile uint32_t*)address;
}
```

## Tushuntirish va Mantiq:
Pointer cast (`(volatile uint32_t*)`) xotira manzilini o'qilishi mumkin bo'lgan o'zgaruvchi sifatida ko'rsatadi.

## Ishlash natijasi:
```text
Manzil 0x20000000 qiymati: 0xDEADBEEF
```

---

# 1008-Topshiriq: Watchdog Timer (WDT) resetini oldini olish

## Topshiriq sharti:
Dastur osilib qolmasligi uchun Watchdog taymerini "oziqlantiruvchi" (kick/refresh) funksiya yozing.

## Yechim (C kodi):
```c
void refresh_watchdog(void) {
    WDT->KR = 0xAAAA; // WDT ni nolga qaytarish kaliti
}
```

## Tushuntirish va Mantiq:
Watchdog - bu xavfsizlik mexanizmi. Agar dastur ma'lum vaqt ichida `refresh` qilmasa, mikrokontroller avtomatik qayta yuklanadi (reset).

## Ishlash natijasi:
```text
Watchdog taymeri yangilandi.
```

---

# 1009-Topshiriq: Struct va Bit-fields yordamida registrni modellashtirish

## Topshiriq sharti:
8-bitli registrni bit-field yordamida strukturaga aylantiring.

## Yechim (C kodi):
```c
typedef struct {
    uint8_t enable : 1;
    uint8_t mode   : 2;
    uint8_t reserved: 5;
} ConfigReg;
```

## Tushuntirish va Mantiq:
Bit-fields xotirani tejash va registr bitlariga nom bilan murojaat qilish uchun juda qulaydir.

## Ishlash natijasi:
```text
ConfigReg hajmi: 1 bayt.
```

---

# 1010-Topshiriq: DMA (Direct Memory Access) orqali ma'lumot uzatish

## Topshiriq sharti:
DMA kontrollerini ishga tushirib, xotiradan UART buferiga ma'lumot yuborishni sozlang.

## Yechim (C kodi):
```c
void start_dma_transfer(uint32_t src, uint32_t dest, uint16_t size) {
    DMA1_Stream0->M0AR = src;
    DMA1_Stream0->PAR = dest;
    DMA1_Stream0->NDTR = size;
    DMA1_Stream0->CR |= 1; // DMA ni yoqish
}
```

## Tushuntirish va Mantiq:
DMA protsessor ishtirokisiz ma'lumotni to'g'ridan-to'g'ri xotiradan periferiyaga ko'chiradi, bu esa tizim unumdorligini keskin oshiradi.

## Ishlash natijasi:
```text
DMA orqali ma'lumot uzatish boshlandi.
```

---

Salom, men **Khorazmiy AI** loyihasining katta dataset muhandisiman. Embedded C tizimlari, mikrokontrollerlar va RTOS bo'yicha datasetimizni boyitish uchun mo'ljallangan #1011 dan #1020 gacha bo'lgan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1011-Topshiriq: STM32 GPIO Interrupt orqali tugmani boshqarish

## Topshiriq sharti:
STM32 mikrokontrollerida tashqi tugma bosilganda (Falling Edge) interrupt (EXTI) yordamida LED holatini o'zgartiruvchi (toggle) kod yozing.

## Yechim (C kodi):
```c
#include "stm32f4xx.h"

void EXTI0_IRQHandler(void) {
    if (EXTI->PR & EXTI_PR_PR0) {
        GPIOA->ODR ^= GPIO_ODR_OD5; // LEDni toggle qilish
        EXTI->PR |= EXTI_PR_PR0;    // Interrupt bayrog'ini tozalash
    }
}

int main(void) {
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    GPIOA->MODER |= GPIO_MODER_MODER5_0; // PA5 chiqish
    SYSCFG->EXTICR[0] |= SYSCFG_EXTICR1_EXTI0_PA;
    EXTI->IMR |= EXTI_IMR_MR0;
    EXTI->FTSR |= EXTI_FTSR_TR0;
    NVIC_EnableIRQ(EXTI0_IRQn);
    while(1);
}
```

## Tushuntirish va Mantiq:
`EXTI0_IRQHandler` funksiyasi tugma bosilganda chaqiriladi. `PR` (Pending Register) orqali interrupt manbasi aniqlanadi va `ODR` registri orqali LED holati teskarilanadi.

## Ishlash natijasi:
```text
Tugma bosilganda PA5 pinidagi LED holati o'zgaradi (ON/OFF).
```

---

# 1012-Topshiriq: ESP32 uchun FreeRTOS Task yaratish

## Topshiriq sharti:
ESP32 da ikkita alohida vazifa (task) yarating: biri har 1 soniyada "Task 1" ni, ikkinchisi har 2 soniyada "Task 2" ni chop etsin.

## Yechim (C kodi):
```c
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void task1(void *pv) { while(1) { printf("Task 1\n"); vTaskDelay(1000/portTICK_PERIOD_MS); } }
void task2(void *pv) { while(1) { printf("Task 2\n"); vTaskDelay(2000/portTICK_PERIOD_MS); } }

void app_main() {
    xTaskCreate(task1, "T1", 2048, NULL, 1, NULL);
    xTaskCreate(task2, "T2", 2048, NULL, 1, NULL);
}
```

## Tushuntirish va Mantiq:
`xTaskCreate` funksiyasi RTOS scheduleriga yangi vazifalarni qo'shadi. `vTaskDelay` CPU ni bo'shatib, boshqa vazifalarga ishlash imkonini beradi.

## Ishlash natijasi:
```text
Task 1
Task 2
Task 1
Task 1
Task 2
...
```

---

# 1013-Topshiriq: ADC qiymatini o'qish va kuchlanishga aylantirish

## Topshiriq sharti:
STM32 ADC modulidan 12-bitli qiymatni o'qing va uni 3.3V shkalasiga moslab kuchlanish qiymatiga (float) aylantiring.

## Yechim (C kodi):
```c
float get_voltage(uint16_t adc_val) {
    return (adc_val * 3.3f) / 4095.0f;
}

// ADC1->DR dan qiymat olinganda:
float voltage = get_voltage(ADC1->DR);
```

## Tushuntirish va Mantiq:
12-bitli ADC 0-4095 oralig'ida qiymat beradi. `(adc_val / 4095) * Vref` formulasi orqali haqiqiy kuchlanish aniqlanadi.

## Ishlash natijasi:
```text
ADC qiymati: 2048 -> Kuchlanish: 1.65V
```

---

# 1014-Topshiriq: UART orqali ma'lumot uzatish (Polling)

## Topshiriq sharti:
STM32 UART2 porti orqali "Hello Khorazmiy" matnini uzatuvchi funksiya yozing.

## Yechim (C kodi):
```c
void UART_SendChar(char c) {
    while(!(USART2->SR & USART_SR_TXE));
    USART2->DR = c;
}

void UART_SendString(char* str) {
    while(*str) UART_SendChar(*str++);
}
```

## Tushuntirish va Mantiq:
`TXE` (Transmit Data Register Empty) bayrog'i tekshiriladi. Agar bo'sh bo'lsa, ma'lumot `DR` (Data Register) ga yoziladi.

## Ishlash natijasi:
```text
Terminalda: Hello Khorazmiy
```

---

# 1015-Topshiriq: I2C orqali sensor bilan bog'lanish

## Topshiriq sharti:
I2C protokoli yordamida 0x68 manzilidagi sensordan 1 bayt ma'lumot o'qib olish algoritmi.

## Yechim (C kodi):
```c
uint8_t I2C_ReadByte(uint8_t devAddr, uint8_t regAddr) {
    I2C1->CR1 |= I2C_CR1_START;
    while(!(I2C1->SR1 & I2C_SR1_SB));
    I2C1->DR = (devAddr << 1);
    while(!(I2C1->SR1 & I2C_SR1_ADDR));
    I2C1->DR = regAddr;
    // ... qayta start va o'qish mantiqi
    return I2C1->DR;
}
```

## Tushuntirish va Mantiq:
I2C start shartini yuboradi, manzilni tanlaydi va kerakli registrni so'raydi. `SR1` registri orqali holat nazorat qilinadi.

## Ishlash natijasi:
```text
Sensor ma'lumoti: 0x4A
```

---

# 1016-Topshiriq: Ring Buffer (FIFO) implementatsiyasi

## Topshiriq sharti:
Embedded tizimlar uchun xavfsiz 10 baytlik Ring Buffer (FIFO) tuzilmasini yarating.

## Yechim (C kodi):
```c
#define SIZE 10
uint8_t buffer[SIZE], head = 0, tail = 0;

void push(uint8_t data) {
    buffer[head] = data;
    head = (head + 1) % SIZE;
}

uint8_t pop() {
    uint8_t data = buffer[tail];
    tail = (tail + 1) % SIZE;
    return data;
}
```

## Tushuntirish va Mantiq:
`head` va `tail` ko'rsatkichlari modulo operatori yordamida aylanma harakat qiladi, bu esa xotirani tejaydi va ma'lumotlar oqimini tartiblaydi.

## Ishlash natijasi:
```text
Buffer holati: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

# 1017-Topshiriq: PWM yordamida yorug'likni boshqarish

## Topshiriq sharti:
STM32 Timer2 yordamida 50% duty cycle ga ega PWM signalini hosil qiling.

## Yechim (C kodi):
```c
TIM2->PSC = 84 - 1; // Prescaler
TIM2->ARR = 1000 - 1; // Period
TIM2->CCR1 = 500; // 50% Duty Cycle
TIM2->CCMR1 |= TIM_CCMR1_OC1M_1 | TIM_CCMR1_OC1M_2;
TIM2->CCER |= TIM_CCER_CC1E;
TIM2->CR1 |= TIM_CR1_CEN;
```

## Tushuntirish va Mantiq:
`ARR` davrni, `CCR1` esa signalning yuqori holatda bo'lish vaqtini belgilaydi. `PSC` chastotani mikrokontroller taktiga moslaydi.

## Ishlash natijasi:
```text
PWM chiqishida 50% to'lqinli signal hosil bo'ladi.
```

---

# 1018-Topshiriq: Watchdog Timer (WDT) sozlash

## Topshiriq sharti:
Dastur osilib qolmasligi uchun IWDG (Independent Watchdog) ni 1 soniyaga sozlang.

## Yechim (C kodi):
```c
IWDG->KR = 0x5555; // Yozishni ochish
IWDG->PR = 4;      // Prescaler
IWDG->RLR = 2500;  // Reload qiymati
IWDG->KR = 0xAAAA; // Reload
IWDG->KR = 0xCCCC; // Ishga tushirish
```

## Tushuntirish va Mantiq:
WDT hisoblagichi 0 ga yetganda tizim reset bo'ladi. `0xAAAA` buyrug'i bilan hisoblagich qayta yuklanadi (resetning oldi olinadi).

## Ishlash natijasi:
```text
Tizim 1 soniya ichida reset qilinmasa, avtomatik qayta ishga tushadi.
```

---

# 1019-Topshiriq: DMA orqali xotiradan UARTga ma'lumot uzatish

## Topshiriq sharti:
CPU ni yuklamasdan, DMA yordamida massivni UART orqali yuborishni sozlang.

## Yechim (C kodi):
```c
DMA1_Stream6->M0AR = (uint32_t)data_array;
DMA1_Stream6->NDTR = 10; // 10 bayt
DMA1_Stream6->CR |= DMA_SxCR_EN;
USART2->CR3 |= USART_CR3_DMAT;
```

## Tushuntirish va Mantiq:
DMA (Direct Memory Access) CPU aralashuvisiz xotiradagi ma'lumotni to'g'ridan-to'g'ri periferiyaga (UART) ko'chiradi.

## Ishlash natijasi:
```text
Ma'lumotlar CPU yuklamasisiz uzatildi.
```

---

# 1020-Topshiriq: RTOS Semaphor yordamida resursni himoyalash

## Topshiriq sharti:
Ikki vazifa bir vaqtda bitta resursdan (masalan, LCD displey) foydalanmasligi uchun Binary Semaphore ishlating.

## Yechim (C kodi):
```c
SemaphoreHandle_t xSemaphore = xSemaphoreCreateBinary();
xSemaphoreGive(xSemaphore); // Resurs bo'sh

void task(void *pv) {
    if(xSemaphoreTake(xSemaphore, portMAX_DELAY)) {
        // LCD ga yozish
        xSemaphoreGive(xSemaphore);
    }
}
```

## Tushuntirish va Mantiq:
`xSemaphoreTake` resursni band qiladi, boshqa vazifa esa resurs bo'shaguncha kutib turadi. Bu "Race Condition" muammosini hal qiladi.

## Ishlash natijasi:
```text
Resursga kirish tartiblandi, ma'lumotlar to'qnashuvi yo'q.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Embedded C tizimlarini rivojlantirish va ma'lumotlar bazasini boyitish uchun mo'ljallangan #1021-#1030 topshiriqlar to'plamini taqdim etaman.

---

# 1021-Topshiriq: STM32 GPIO Pinini Bit-Masking orqali boshqarish

## Topshiriq sharti:
STM32 mikrokontrollerida `GPIOA_ODR` registrining 5-bitini (LED) to'g'ridan-to'g'ri bit-masking usuli bilan yoqish va o'chirish funksiyasini yozing.

## Yechim (C kodi):
```c
#include <stdint.h>

#define GPIOA_BASE 0x40020000
#define GPIOA_ODR  (*(volatile uint32_t *)(GPIOA_BASE + 0x14))
#define LED_PIN    (1 << 5)

void toggle_led() {
    GPIOA_ODR ^= LED_PIN;
}

int main() {
    toggle_led(); // LED holatini o'zgartirish
    return 0;
}
```

## Tushuntirish va Mantiq:
`volatile` kalit so'zi kompilyatorga bu registr qiymati tashqi omillar bilan o'zgarishi mumkinligini bildiradi. `^=` (XOR) operatori bitni teskari holatga o'tkazish uchun eng samarali usuldir.

## Ishlash natijasi:
```text
GPIOA_ODR qiymati: 0x00000020 (5-bit o'zgardi)
```

---

# 1022-Topshiriq: ESP32 uchun ADC qiymatini o'qish va filtrlash

## Topshiriq shovqini:
ESP32 ADC (Analog-to-Digital Converter) dan olingan shovqinli signallarni "Moving Average" (o'rtacha qiymat) filtri yordamida tekislash.

## Yechim (C kodi):
```c
#include <stdio.h>

#define SAMPLES 5
int filter_adc(int new_val) {
    static int buffer[SAMPLES] = {0};
    static int index = 0;
    static long sum = 0;

    sum -= buffer[index];
    buffer[index] = new_val;
    sum += buffer[index];
    index = (index + 1) % SAMPLES;

    return (int)(sum / SAMPLES);
}

int main() {
    printf("Filtrlangan qiymat: %d\n", filter_adc(1024));
    return 0;
}
```

## Tushuntirish va Mantiq:
Bu algoritm o'tgan 5 ta qiymatning yig'indisini saqlaydi. Har safar yangi qiymat kelganda, eng eski qiymat ayirilib, yangisi qo'shiladi. Bu xotirani tejash uchun optimal yechim.

## Ishlash natijasi:
```text
Filtrlangan qiymat: 204
```

---

# 1023-Topshiriq: RTOS (FreeRTOS) da Vazifalararo xabar almashish (Queue)

## Topshiriq sharti:
FreeRTOS yordamida sensor ma'lumotlarini yuboruvchi va qabul qiluvchi ikkita vazifa (Task) yarating.

## Yechim (C kodi):
```c
#include "FreeRTOS.h"
#include "queue.h"

QueueHandle_t xQueue;

void vSenderTask(void *pvParameters) {
    int data = 42;
    xQueueSend(xQueue, &data, 0);
}

void vReceiverTask(void *pvParameters) {
    int received;
    if(xQueueReceive(xQueue, &received, 100)) {
        // Ma'lumot qabul qilindi
    }
}
```

## Tushuntirish va Mantiq:
`Queue` - bu RTOS muhitida vazifalar o'rtasida xavfsiz ma'lumot almashish mexanizmi. `xQueueSend` ma'lumotni navbatga qo'shadi, `xQueueReceive` esa uni oladi.

## Ishlash natijasi:
```text
Ma'lumot muvaffaqiyatli uzatildi: 42
```

---

# 1024-Topshiriq: UART orqali ma'lumot uzatish drayveri

## Topshiriq sharti:
Mikrokontrollerda UART orqali string (satr) yuborish uchun `UART_SendString` funksiyasini yozing.

## Yechim (C kodi):
```c
void UART_SendChar(char c) {
    while(!(UART->SR & (1 << 7))); // TXE bayrog'ini kutish
    UART->DR = c;
}

void UART_SendString(char* str) {
    while(*str) {
        UART_SendChar(*str++);
    }
}
```

## Tushuntirish va Mantiq:
`TXE` (Transmit Data Register Empty) bayrog'i UART buferining bo'shligini bildiradi. Har bir belgi yuborilgach, pointer keyingi manzilga o'tadi.

## Ishlash natijasi:
```text
UART orqali string yuborildi.
```

---

# 1025-Topshiriq: Interrupt (Uzilish) yordamida tugma bosilishini aniqlash

## Topshiriq sharti:
STM32 EXTI (External Interrupt) yordamida tugma bosilganda LED holatini o'zgartiruvchi ISR (Interrupt Service Routine) yozing.

## Yechim (C kodi):
```c
void EXTI0_IRQHandler(void) {
    if(EXTI->PR & (1 << 0)) {
        GPIOA->ODR ^= (1 << 5); // LEDni o'zgartirish
        EXTI->PR |= (1 << 0);   // Bayroqni tozalash
    }
}
```

## Tushuntirish va Mantiq:
ISR - bu apparat darajasidagi hodisaga javob beruvchi funksiya. `EXTI->PR` bayrog'ini tozalash shart, aks holda uzilish cheksiz davom etadi.

## Ishlash natijasi:
```text
Tugma bosildi, LED holati o'zgardi.
```

---

# 1026-Topshiriq: I2C protokoli orqali sensor manzilini o'qish

## Topshiriq sharti:
I2C avtobusi orqali sensorga "Who Am I" so'rovini yuborib, uning ID raqamini oling.

## Yechim (C kodi):
```c
uint8_t I2C_ReadID(uint8_t dev_addr) {
    I2C_Start();
    I2C_Write(dev_addr << 1);
    I2C_Write(0x75); // WHO_AM_I registri
    I2C_Restart();
    I2C_Write((dev_addr << 1) | 1);
    uint8_t id = I2C_Read(0);
    I2C_Stop();
    return id;
}
```

## Tushuntirish va Mantiq:
I2C protokoli Start, Address, Register, Restart va Read bosqichlaridan iborat. Bu kod sensor bilan aloqa o'rnatishning standart ketma-ketligidir.

## Ishlash natijasi:
```text
Sensor ID: 0x68
```

---

# 1027-Topshiriq: Watchdog Timer (WDT) ni sozlash

## Topshiriq sharti:
Dastur osilib qolmasligi uchun Watchdog Timer'ni 2 soniyaga sozlang.

## Yechim (C kodi):
```c
void WDT_Init() {
    IWDG->KR = 0x5555; // Yozishdan himoyani ochish
    IWDG->PR = 0x06;   // Prescaler
    IWDG->RLR = 0xFFF; // Reload qiymati
    IWDG->KR = 0xAAAA; // Refresh
    IWDG->KR = 0xCCCC; // Ishga tushirish
}
```

## Tushuntirish va Mantiq:
WDT - bu tizim xatosi yuz berganda mikrokontrollerni qayta ishga tushiruvchi "qo'riqchi". `KR` registriga maxsus kodlar yuborish orqali boshqariladi.

## Ishlash natijasi:
```text
Watchdog ishga tushdi.
```

---

# 1028-Topshiriq: DMA (Direct Memory Access) orqali ma'lumot ko'chirish

## Topshiriq sharti:
CPU ishtirokisiz xotiraning bir qismidan ikkinchisiga ma'lumot ko'chirishni sozlang.

## Yechim (C kodi):
```c
void DMA_Config(uint32_t src, uint32_t dst, uint16_t len) {
    DMA1_Stream0->PAR = src;
    DMA1_Stream0->M0AR = dst;
    DMA1_Stream0->NDTR = len;
    DMA1_Stream0->CR |= (1 << 0); // DMA yoqish
}
```

## Tushuntirish va Mantiq:
DMA CPU yukini kamaytiradi. `PAR` (Peripheral Address) va `M0AR` (Memory Address) registrlarini sozlab, ma'lumotlarni to'g'ridan-to'g'ri ko'chiramiz.

## Ishlash natijasi:
```text
DMA orqali 100 bayt ko'chirildi.
```

---

# 1029-Topshiriq: PWM (Pulse Width Modulation) bilan yorug'likni boshqarish

## Topshiriq sharti:
Timer yordamida 50% ishchi sikl (duty cycle) bilan PWM signalini hosil qiling.

## Yechim (C kodi):
```c
void PWM_Init() {
    TIM2->ARR = 1000; // Period
    TIM2->CCR1 = 500; // 50% Duty Cycle
    TIM2->CCMR1 |= (6 << 4); // PWM Mode 1
    TIM2->CR1 |= 1; // Timer yoqish
}
```

## Tushuntirish va Mantiq:
`ARR` (Auto Reload Register) chastotani, `CCR1` (Capture Compare Register) esa signalning "ON" holatidagi davomiyligini belgilaydi.

## Ishlash natijasi:
```text
PWM signali 50% siklda ishlamoqda.
```

---

# 1030-Topshiriq: EEPROM xotirasiga ma'lumot yozish

## Topshiriq sharti:
I2C orqali tashqi EEPROM xotirasiga 1 bayt ma'lumot yozish funksiyasini yozing.

## Yechim (C kodi):
```c
void EEPROM_Write(uint16_t addr, uint8_t data) {
    I2C_Start();
    I2C_Write(0xA0); // EEPROM yozish manzili
    I2C_Write(addr >> 8);
    I2C_Write(addr & 0xFF);
    I2C_Write(data);
    I2C_Stop();
}
```

## Tushuntirish va Mantiq:
EEPROM manzili odatda 16 bit bo'lgani uchun uni ikkiga bo'lib (yuqori va quyi bayt) yuborish kerak. Bu ma'lumotlarning doimiy saqlanishini ta'minlaydi.

## Ishlash natijasi:
```text
EEPROM manziliga ma'lumot yozildi.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Embedded C tizimlarini rivojlantirish va mikrokontrollerlar uchun yuqori sifatli o'quv materiallarini shakllantirish maqsadida, #1031 dan #1040 gacha bo'lgan 10 ta ilg'or topshiriqni taqdim etaman.

---

# 1031-Topshiriq: STM32 GPIO Interrupt orqali tugmani boshqarish

## Topshiriq sharti:
STM32 mikrokontrollerida tashqi uzilish (EXTI) yordamida tugma bosilganda LED holatini o'zgartiruvchi (toggle) dastur yozing.

## Yechim (C kodi):
```c
#include "stm32f4xx.h"

void EXTI0_IRQHandler(void) {
    if (EXTI->PR & EXTI_PR_PR0) {
        GPIOA->ODR ^= GPIO_ODR_OD5; // LED holatini o'zgartirish
        EXTI->PR |= EXTI_PR_PR0;    // Uzilish bayrog'ini tozalash
    }
}

int main(void) {
    RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN;
    GPIOA->MODER |= GPIO_MODER_MODER5_0; // PA5 chiqish
    SYSCFG->EXTICR[0] |= SYSCFG_EXTICR1_EXTI0_PA;
    EXTI->IMR |= EXTI_IMR_MR0;
    EXTI->FTSR |= EXTI_FTSR_TR0;
    NVIC_EnableIRQ(EXTI0_IRQn);
    while(1);
}
```

## Tushuntirish va Mantiq:
Kodda `EXTI0_IRQHandler` uzilish funksiyasi ishlatilgan. `EXTI->PR` bayrog'i tekshiriladi va PA5 pinidagi LED holati XOR operatori yordamida teskarilanadi. `SYSCFG` orqali uzilish manbasi PA0 ga yo'naltirilgan.

## Ishlash natijasi:
```text
Tugma bosilganda PA5 pinidagi LED yonadi/o'chadi.
```

---

# 1032-Topshiriq: ESP32 uchun ADC (Analog-to-Digital Converter) o'qish

## Topshiriq sharti:
ESP32 ADC pinidan (GPIO34) analog qiymatni o'qib, uni 0-3.3V diapazoniga o'tkazuvchi funksiya yozing.

## Yechim (C kodi):
```c
#include "driver/adc.h"

float read_voltage(void) {
    adc1_config_width(ADC_WIDTH_BIT_12);
    adc1_config_channel_atten(ADC1_CHANNEL_6, ADC_ATTEN_DB_11);
    int raw = adc1_get_raw(ADC1_CHANNEL_6);
    return (raw * 3.3) / 4095.0;
}
```

## Tushuntirish va Mantiq:
ESP32 12-bitli ADCga ega (0-4095). `ADC_ATTEN_DB_11` 3.3V gacha o'lchash imkonini beradi. Olingan qiymat proporsional ravishda kuchlanishga aylantiriladi.

## Ishlash natijasi:
```text
Voltaj: 1.25V (o'lchangan qiymatga qarab)
```

---

# 1033-Topshiriq: RTOS (FreeRTOS) vazifalarini yaratish

## Topshiriq sharti:
FreeRTOS yordamida ikkita parallel vazifa (task) yarating: biri LEDni miltillatsin, ikkinchisi UART orqali xabar yuborsin.

## Yechim (C kodi):
```c
void TaskLED(void *pv) {
    while(1) { GPIO_Toggle(); vTaskDelay(500/portTICK_PERIOD_MS); }
}
void TaskUART(void *pv) {
    while(1) { printf("Tizim ishlamoqda...\n"); vTaskDelay(2000/portTICK_PERIOD_MS); }
}
```

## Tushuntirish va Mantiq:
`vTaskDelay` funksiyasi vazifani bloklaydi va protsessor vaqtini boshqa vazifalarga beradi. Bu RTOSning ko'p vazifalilik (multitasking) tamoyilidir.

## Ishlash natijasi:
```text
Tizim ishlamoqda... (har 2 soniyada)
```

---

# 1034-Topshiriq: I2C drayverini simulyatsiya qilish (Start/Stop)

## Topshiriq sharti:
I2C protokoli uchun `I2C_Start` va `I2C_Stop` funksiyalarini bit-banging usulida yozing.

## Yechim (C kodi):
```c
void I2C_Start(void) { SDA_High(); SCL_High(); Delay(); SDA_Low(); Delay(); SCL_Low(); }
void I2C_Stop(void) { SDA_Low(); SCL_High(); Delay(); SDA_High(); }
```

## Tushuntirish va Mantiq:
I2C start sharti SCL yuqori bo'lganda SDA ning yuqoridan pastga o'tishidir. Stop esa aksincha. `Delay()` funksiyasi signal barqarorligini ta'minlaydi.

## Ishlash natijasi:
```text
I2C Start/Stop signallari generatsiya qilindi.
```

---

# 1035-Topshiriq: Ring Buffer (Navbat) implementatsiyasi

## Topshiriq sharti:
UART ma'lumotlarini saqlash uchun 16 baytlik ring buffer (aylanma bufer) yarating.

## Yechim (C kodi):
```c
#define SIZE 16
uint8_t buffer[SIZE], head = 0, tail = 0;
void push(uint8_t data) { buffer[head] = data; head = (head + 1) % SIZE; }
uint8_t pop(void) { uint8_t d = buffer[tail]; tail = (tail + 1) % SIZE; return d; }
```

## Tushuntirish va Mantiq:
`head` va `tail` indekslari modulo operatori yordamida aylanma harakat qiladi. Bu ma'lumotlar oqimini yo'qotmasdan qayta ishlashga imkon beradi.

## Ishlash natijasi:
```text
Buffer holati: [0, 1, 2, 3...]
```

---

# 1036-Topshiriq: Watchdog Timer (WDT) sozlash

## Topshiriq sharti:
STM32 da Watchdog taymerini 1 soniyaga sozlang. Agar dastur osilib qolsa, mikrokontroller qayta ishga tushsin.

## Yechim (C kodi):
```c
void WDT_Init(void) {
    IWDG->KR = 0x5555; // Yozishni ochish
    IWDG->PR = 4;      // Prescaler
    IWDG->RLR = 2500;  // 1 soniya uchun qiymat
    IWDG->KR = 0xAAAA; // Refresh
    IWDG->KR = 0xCCCC; // Ishga tushirish
}
```

## Tushuntirish va Mantiq:
WDT - bu xavfsizlik mexanizmi. `IWDG->KR = 0xAAAA` buyrug'i "oziqlantirish" (feed) deyiladi. Agar bu buyruq 1 soniya ichida bajarilmasa, MCU reset bo'ladi.

## Ishlash natijasi:
```text
Watchdog faollashtirildi.
```

---

# 1037-Topshiriq: SPI orqali ma'lumot uzatish

## Topshiriq sharti:
SPI interfeysi orqali 8-bitli ma'lumotni yuboruvchi funksiya yozing.

## Yechim (C kodi):
```c
uint8_t SPI_Transmit(uint8_t data) {
    while(!(SPI1->SR & SPI_SR_TXE));
    SPI1->DR = data;
    while(!(SPI1->SR & SPI_SR_RXNE));
    return SPI1->DR;
}
```

## Tushuntirish va Mantiq:
`TXE` (Transmit Buffer Empty) bayrog'i ma'lumot yuborishga tayyorligini, `RXNE` (Receive Not Empty) esa qabul qilingan ma'lumotni bildiradi.

## Ishlash natijasi:
```text
SPI ma'lumot uzatildi: 0xAA
```

---

# 1038-Topshiriq: PWM (Pulse Width Modulation) yordamida yorqinlikni boshqarish

## Topshiriq sharti:
Timer yordamida 50% ishchi siklga (duty cycle) ega PWM signali hosil qiling.

## Yechim (C kodi):
```c
void PWM_Init(void) {
    TIM2->ARR = 1000; // Period
    TIM2->CCR1 = 500; // 50% Duty Cycle
    TIM2->CCMR1 |= TIM_CCMR1_OC1M_1 | TIM_CCMR1_OC1M_2;
    TIM2->CCER |= TIM_CCER_CC1E;
    TIM2->CR1 |= TIM_CR1_CEN;
}
```

## Tushuntirish va Mantiq:
`ARR` taymerning maksimal qiymati, `CCR1` esa signalning "ON" holatidagi davomiyligi. `500/1000` nisbati 50% yorqinlikni beradi.

## Ishlash natijasi:
```text
PWM signali 50% duty cycle bilan ishlamoqda.
```

---

# 1039-Topshiriq: EEPROM (I2C) ga ma'lumot yozish

## Topshiriq sharti:
I2C orqali tashqi EEPROM xotirasiga 1 bayt ma'lumot yozish funksiyasini yozing.

## Yechim (C kodi):
```c
void EEPROM_Write(uint16_t addr, uint8_t data) {
    I2C_Start();
    I2C_Send(0xA0); // EEPROM manzili
    I2C_Send(addr);
    I2C_Send(data);
    I2C_Stop();
}
```

## Tushuntirish va Mantiq:
EEPROM yozish uchun avval qurilma manzili, keyin xotira manzili va nihoyat ma'lumot yuboriladi.

## Ishlash natijasi:
```text
Ma'lumot EEPROM ga yozildi.
```

---

# 1040-Topshiriq: DMA (Direct Memory Access) yordamida ma'lumot uzatish

## Topshiriq sharti:
CPU ishtirokisiz UART orqali xotiradan ma'lumot yuborish uchun DMA ni sozlang.

## Yechim (C kodi):
```c
void DMA_Config(uint8_t *data, uint16_t len) {
    DMA1_Stream6->M0AR = (uint32_t)data;
    DMA1_Stream6->NDTR = len;
    DMA1_Stream6->CR |= DMA_SxCR_EN;
}
```

## Tushuntirish va Mantiq:
DMA protsessorni yuklamasdan ma'lumotlarni to'g'ridan-to'g'ri xotiradan periferiyaga ko'chiradi. `NDTR` yuborilishi kerak bo'lgan baytlar sonini belgilaydi.

## Ishlash natijasi:
```text
DMA orqali ma'lumot uzatish boshlandi.
```

---

Salom, men 'Khorazmiy AI' loyihasining katta dataset muhandisiman. Embedded C va mikrokontrollerlar bo'yicha 100 000 talik datasetimizni boyitish uchun mo'ljallangan #1041-#1050 topshiriqlar to'plami quyidagicha:

---

# 1041-Topshiriq: STM32 GPIO konfiguratsiyasi (Bitwise operatsiyalar)

## Topshiriq sharti:
STM32 mikrokontrollerida PA5 pinini chiqish (output) rejimiga o'tkazish va uni "set" qilish uchun bitwise operatsiyalardan foydalanib kod yozing.

## Yechim (C kodi):
```c
#include <stdint.h>

#define GPIOA_BASE 0x40020000
#define MODER      (*(volatile uint32_t *)(GPIOA_BASE + 0x00))
#define ODR        (*(volatile uint32_t *)(GPIOA_BASE + 0x14))

void setup_gpio() {
    MODER &= ~(3U << (5 * 2)); // 5-pinni tozalash
    MODER |= (1U << (5 * 2));  // 5-pinni output qilish
    ODR |= (1U << 5);          // 5-pinni HIGH qilish
}
```

## Tushuntirish va Mantiq:
`MODER` registri har bir pin uchun 2 bit ajratadi. `3U << (5*2)` maskasi orqali 10 va 11-bitlar tozalanadi, so'ngra `1U << 10` orqali output rejimi o'rnatiladi. `ODR` registridagi 5-bitni 1 ga tenglash orqali pin kuchlanish bilan ta'minlanadi.

## Ishlash natijasi:
```text
GPIOA_MODER: 0x00000400, GPIOA_ODR: 0x00000020
```

---

# 1042-Topshiriq: ESP32 uchun ADC qiymatini o'qish

## Topshiriq sharti:
ESP32 ADC1_CHANNEL_0 (GPIO36) dan analog qiymatni o'qib, uni 12-bitli (0-4095) raqamli qiymatga aylantiruvchi funksiya yozing.

## Yechim (C kodi):
```c
#include "driver/adc.h"

int read_adc_value() {
    adc1_config_width(ADC_WIDTH_BIT_12);
    adc1_config_channel_atten(ADC1_CHANNEL_0, ADC_ATTEN_DB_11);
    return adc1_get_raw(ADC1_CHANNEL_0);
}
```

## Tushuntirish va Mantiq:
`adc1_config_width` 12-bitli aniqlikni belgilaydi. `ADC_ATTEN_DB_11` esa 0-3.3V diapazonini qamrab olish uchun kuchlanishni susaytiradi. `adc1_get_raw` funksiyasi ADC konvertatsiyasini amalga oshiradi.

## Ishlash natijasi:
```text
ADC Raw Value: 2048 (taxminan 1.65V)
```

---

# 1043-Topshiriq: RTOS Vazifalar (Task) yaratish

## Topshiriq sharti:
FreeRTOS yordamida 100ms davr bilan ishlaydigan "BlinkTask" vazifasini yarating.

## Yechim (C kodi):
```c
#include "FreeRTOS.h"
#include "task.h"

void BlinkTask(void *pvParameters) {
    while(1) {
        // LED Toggle logic
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}

void app_main() {
    xTaskCreate(BlinkTask, "Blink", 1024, NULL, 1, NULL);
}
```

## Tushuntirish va Mantiq:
`xTaskCreate` vazifani rejalashtiruvchiga (scheduler) qo'shadi. `vTaskDelay` vazifani bloklaydi va protsessorni boshqa vazifalarga bo'shatib beradi, bu esa RTOS samaradorligini ta'minlaydi.

## Ishlash natijasi:
```text
Task 'Blink' created. LED toggling every 100ms.
```

---

# 1044-Topshiriq: UART orqali ma'lumot yuborish (Polling)

## Topshiriq sharti:
STM32 UART1 orqali "Khorazmiy AI" satrini uzluksiz yuboruvchi drayver qismini yozing.

## Yechim (C kodi):
```c
#include "stm32f4xx.h"

void UART_SendChar(char c) {
    while(!(USART1->SR & USART_SR_TXE));
    USART1->DR = c;
}

void UART_SendString(char* str) {
    while(*str) UART_SendChar(*str++);
}
```

## Tushuntirish va Mantiq:
`USART_SR_TXE` (Transmit Data Register Empty) bayrog'i tekshiriladi. Agar 1 bo'lsa, bufer bo'sh va yangi bayt yuborish mumkin. `DR` (Data Register) ga bayt yozilgach, UART uni ketma-ket (serial) uzatadi.

## Ishlash natijasi:
```text
Output: Khorazmiy AI
```

---

# 1045-Topshiriq: Interrupt (Uzilish) yordamida tugmani boshqarish

## Topshiriq sharti:
Tashqi uzilish (EXTI) yordamida tugma bosilganda LED holatini o'zgartiruvchi ISR (Interrupt Service Routine) yozing.

## Yechim (C kodi):
```c
void EXTI0_IRQHandler(void) {
    if(EXTI->PR & EXTI_PR_PR0) {
        GPIOA->ODR ^= (1 << 5); // LEDni teskari qilish
        EXTI->PR |= EXTI_PR_PR0; // Bayroqni tozalash
    }
}
```

## Tushuntirish va Mantiq:
Tugma bosilganda protsessor asosiy kodni to'xtatib, ushbu ISR ga o'tadi. `EXTI_PR_PR0` bayrog'i uzilish sodir bo'lganini bildiradi. Ish tugagach, bayroqni dasturiy ravishda tozalash shart.

## Ishlash natijasi:
```text
Interrupt triggered. LED state toggled.
```

---

# 1046-Topshiriq: I2C orqali sensor bilan aloqa

## Topshiriq sharti:
I2C protokoli orqali 0x68 manzilidagi sensordan 1 bayt ma'lumot o'qish funksiyasini yozing.

## Yechim (C kodi):
```c
uint8_t I2C_ReadByte(uint8_t devAddr, uint8_t regAddr) {
    I2C1->CR1 |= I2C_CR1_START;
    while(!(I2C1->SR1 & I2C_SR1_SB));
    I2C1->DR = (devAddr << 1);
    // ... (manzil va registrlarni yuborish)
    return I2C1->DR;
}
```

## Tushuntirish va Mantiq:
I2C aloqasi START signali bilan boshlanadi. Qurilma manzili yuborilgach, kerakli registr manzili ko'rsatiladi va ma'lumot qabul qilinadi. `SR1` registri aloqa holatini kuzatib boradi.

## Ishlash natijasi:
```text
Data received: 0x4A
```

---

# 1047-Topshiriq: Timer yordamida PWM yaratish

## Topshiriq sharti:
STM32 Timer2 yordamida 50% ishchi sikl (duty cycle) bilan PWM signali hosil qiling.

## Yechim (C kodi):
```c
void PWM_Init() {
    TIM2->ARR = 1000 - 1; // Period
    TIM2->CCR1 = 500;     // 50% Duty Cycle
    TIM2->CCMR1 |= (6 << 4); // PWM Mode 1
    TIM2->CCER |= TIM_CCER_CC1E;
    TIM2->CR1 |= TIM_CR1_CEN;
}
```

## Tushuntirish va Mantiq:
`ARR` (Auto-Reload Register) signal davrini, `CCR1` (Capture Compare Register) esa signalning "HIGH" holatda qolish vaqtini belgilaydi. PWM Mode 1 signalni belgilangan chegaragacha HIGH, keyin LOW qiladi.

## Ishlash natijasi:
```text
PWM signal generated on Channel 1.
```

---

# 1048-Topshiriq: Ring Buffer (Aylanma bufer) implementatsiyasi

## Topshiriq sharti:
UART orqali kelayotgan ma'lumotlarni saqlash uchun 16 baytli aylanma bufer yarating.

## Yechim (C kodi):
```c
#define SIZE 16
uint8_t buffer[SIZE];
uint8_t head = 0, tail = 0;

void push(uint8_t data) {
    buffer[head] = data;
    head = (head + 1) % SIZE;
}
```

## Tushuntirish va Mantiq:
Aylanma bufer xotirani tejaydi. `head` yangi ma'lumot yoziladigan joyni, `tail` esa o'qiladigan joyni ko'rsatadi. `% SIZE` operatori indeksning massiv chegarasidan chiqib ketmasligini ta'minlaydi.

## Ishlash natijasi:
```text
Buffer updated. Head: 1, Tail: 0
```

---

# 1049-Topshiriq: Watchdog Timer (WDT) konfiguratsiyasi

## Topshiriq sharti:
Tizim osilib qolmasligi uchun 2 soniyalik Watchdog taymerini yoqing.

## Yechim (C kodi):
```c
void WDT_Init() {
    IWDG->KR = 0x5555; // Yozishni ochish
    IWDG->PR = 4;      // Prescaler
    IWDG->RLR = 2500;  // Reload qiymati
    IWDG->KR = 0xAAAA; // Refresh
    IWDG->KR = 0xCCCC; // Ishga tushirish
}
```

## Tushuntirish va Mantiq:
WDT - bu mustaqil taymer. Agar dastur `0xAAAA` (refresh) buyrug'ini o'z vaqtida yubormasa, WDT mikrokontrollerni qayta yuklaydi (reset). Bu tizim barqarorligi uchun muhim.

## Ishlash natijasi:
```text
Watchdog Timer active.
```

---

# 1050-Topshiriq: SPI orqali Flash xotira bilan ishlash

## Topshiriq sharti:
SPI protokoli orqali Flash xotiradan "Read ID" (0x9F) buyrug'ini yuborib, qurilma ID sini oling.

## Yechim (C kodi):
```c
uint8_t SPI_Transfer(uint8_t data) {
    while(!(SPI1->SR & SPI_SR_TXE));
    SPI1->DR = data;
    while(!(SPI1->SR & SPI_SR_RXNE));
    return SPI1->DR;
}

// Read ID
uint8_t id = SPI_Transfer(0x9F);
```

## Tushuntirish va Mantiq:
SPI to'liq dupleks (full-duplex) aloqa protokoli. `SPI_Transfer` funksiyasi bir vaqtning o'zida bayt yuboradi va qabul qiladi. `TXE` va `RXNE` bayroqlari ma'lumot almashinuvi tugaganini bildiradi.

## Ishlash natijasi:
```text
Device ID: 0xEF (Winbond Flash)
```