# Go (Golang) Dasturlash Tili: Mukammal Qo'llanma va Ensiklopediya
## (Noldan Yuqori Yuklamali Tizimlar, Goroutines, Channels, Mikroservislar va AI Infratuzilmasi)

> **Muallif:** Google Go Jamoasi (Robert Griesemer, Rob Pike, Ken Thompson) Standartlari Asosida  
> **Standart:** Go 1.22+ / 1.23+  
> **Asosiy yo'nalish:** Sodda va toza sintaksis, O'ta tez kompilyatsiya, Yengil ko'p oqimlilik (Goroutines & Channels), Yuqori unumdorlikdagi tarmoq backend serverlari va bulutli AI infratuzilmasi (Docker, Kubernetes asosi).

---

## MUNDARIJA

1. [1-Bob: Go Falsafasi — Nega Sodda Kod Eng Yaxshisi?](#1-bob)
2. [2-Bob: O'zgaruvchilar, Turlar va Boshqaruv Konstruksiyalari](#2-bob)
3. [3-Bob: Slices, Massivlar va Map Kolleksiyalari](#3-bob)
4. [4-Bob: Funksiyalar, Ko'p Qiymat Qaytarish va `defer`](#4-bob)
5. [5-Bob: Ko'rsatkichlar (Pointers) va Xotira Samaradorligi](#5-bob)
6. [6-Bob: Strukturalar (Structs) va Metodlar](#6-bob)
7. [7-Bob: Implitsit Interfeyslar (Interfaces) va Duck Typing](#7-bob)
8. [8-Bob: Xatoliklarni Boshqarish: `error` va `panic/recover`](#8-bob)
9. [9-Bob: Go Generiklari (`any`, `comparable`, constraints)](#9-bob)
10. [10-Bob: Go Concurrency: Goroutines va `sync.WaitGroup`](#10-bob)
11. [11-Bob: Kanallar (Channels) va `select` Konstruksiyasi](#11-bob)
12. [12-Bob: `sync` Paketi: Mutex, RWMutex, Once va Atomic](#12-bob)
13. [13-Bob: `context.Context` — Bekor qilish va Timeoutlar](#13-bob)
14. [14-Bob: HTTP Serverlar, REST API va JSON Bilan Ishlash](#14-bob)
15. [15-Bob: Go da AI Infratuzilmasi: Model Serving va High-Throughput API](#15-bob)

---

### 1-Bob: Go Falsafasi — Nega Sodda Kod Eng Yaxshisi?
Go tili 2007-yilda Google muhandislari (C tili asoschilari Ken Thompson va Rob Pike) tomonidan yaratilgan.
Go ning asosiy shiori: **"Kamroq vosita, yuqori tartib va o'qilishi oson kod"**.
- Ortiqcha murakkab merosxo'rlik (OOP inheritance) yo'q.
- Sekin kompilyatsiya yo'q (Go sekundiga yuz minglab qator kodni mashina tiliga o'giradi).
- Xotirani avtomatik tozalovchi (Garbage Collector) 1 millisekunddan kam kechikish bilan ishlaydi.

---

### 2-Bob: Goroutines va Kanallar (Channels)
Go ning eng kuchli ustuni — **Goroutine**lar:
- Oddiy operatsion tizim oqimi (Thread) 1–2 MB xotira talab qilsa, bitta Goroutine atigi **2 KB** xotira bilan boshlanadi!
- Bitta noutbukda bir vaqtning o'zida **100,000 ta Goroutine**ni parallel ishga tushirish mumkin.

Mashhur Go shiori:
> *"Do not communicate by sharing memory; instead, share memory by communicating."*  
> *(Xotirani bo'lishish orqali muloqot qilmang; muloqot qilish orqali xotirani bo'lishing.)*

---

### 3-Bob: Go da AI Infratuzilmasi va Model Serving
Zamonaviy sun'iy intellekt dunyosida:
- Python modelni o'qitish uchun ishlatilsa,
- **Go tili** o'qitilgan modellarni soniyasiga o'n minglab foydalanuvchilarga tarqatuvchi (Model Serving, High-concurrency Reverse Proxy, gRPC Streaming) orqa tizimlar uchun ishlatiladi.
- Docker, Kubernetes, Prometheus, Terraform kabi dunyo infratuzilmasi 100% Go tilida yozilgan.

---

> **Ushbu ensiklopediya 1,000 ta amaliy Go topshirig'ining nazariy poydevoridir.**
