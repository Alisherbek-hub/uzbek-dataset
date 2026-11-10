# Ruby: Mukammal Ensiklopediya va Fundamental Dasturlash Qo'llanmasi
**Loyiha:** Khorazmiy AI — O'zbek Tilidagi Katta Dasturlash Dataseti  
**Muallif:** Khorazmiy AI Ruby Dataset Specialist  
**Versiya:** Ruby 3.2 / 3.3+ (YJIT, Ractors, Rails 7.1/8.0 arxitekturasi)  
**Qamrovi:** Ruby falsafasi va obyeklar modeli, YARV va YJIT virtual mashinalari, Garbage Collection (GC), Metaprogramming va DSL muhandisligi, Bloklar va Funksional uslub, Ruby on Rails (Full-stack va API), Ko'p oqimli arxitektura (GVL, Fibers, Ractor), Xavfsizlik va zamonaviy AI startaplar integratsiyasi.

---

## Mundarija
1. [Ruby Falsafasi, Tarixi va Madaniyati](#1-ruby-falsafasi-tarixi-va-madaniyati)
2. [Virtual Mashina Arxitekturasi: YARV, Baytkod va YJIT](#2-virtual-mashina-arxitekturasi-yarv-baytkod-va-yjit)
3. [Mukammal Obyekt Modeli: "Hamma narsa Obyekt"](#3-mukammal-obyekt-modeli-hamma-narsa-obyekt)
4. [Xotira Boshqaruvi va Garbage Collection (GC)](#4-xotira-boshqaruvi-va-garbage-collection-gc)
5. [Bloklar, Procs, Lambdalar va Funksional Imkoniyatlar](#5-bloklar-procs-lambdalar-va-funksional-imkoniyatlar)
6. [Metaprogramming va Domain-Specific Languages (DSL)](#6-metaprogramming-va-domain-specific-languages-dsl)
7. [Ruby on Rails: Zamonaviy Veb Startaplar Qiroli](#7-ruby-on-rails-zamonaviy-veb-startaplar-qiroli)
8. [Konkurentlik va Parallelizm: GVL, Fibers va Ractor](#8-konkurentlik-va-parallelizm-gvl-fibers-va-ractor)
9. [Korxona Darajasidagi Xavfsizlik va Unumdorlik](#9-korxona-darajasidagi-xavfsizlik-va-unumdorlik)
10. [Sun'iy Intellekt Davrida Ruby va Startap Arxitekturasi](#10-suniy-intellekt-davrida-ruby-va-startap-arxitekturasi)

---

## 1. Ruby Falsafasi, Tarixi va Madaniyati

Ruby dasturlash tili 1993-yilda yaponiyalik dasturchi Yukihiro Matsumoto ("Matz") tomonidan ishlab chiqilgan va 1995-yilda ommaga taqdim etilgan. Matz tilni yaratishda Perl, Smalltalk, Eiffel, Ada va Lisp tillarining eng kuchli jihatlarini birlashtirgan.

### 1.1. "Developer Happiness" (Dasturchi Baxti) Tamoyili
Matzning asosiy maqsadi dasturni kompyuter uchun emas, balki inson tafakkuriga mos, yozilishi tabiiy va o'qilishi yoqimli qilish edi:
> "Ruby kompyuter yukini yengillatish uchun emas, inson mehnatini quvontirish, dasturchi stressini kamaytirish va ijodiy erkinlik berish uchun yaratilgan."

Ruby madaniyatida mashhur **MINASWAN** shiori mavjud: *"Matz is nice and so we are nice"* (Matz xushmuomala, demak biz ham bir-birimizga xushmuomalamiz). Ushbu tamoyil jahon Ruby hamjamiyatining birdamligi va ochiqligini belgilab bergan.

### 1.2. Sintaksis Nafosati
Ruby-da ortiqcha qavslar, nuqtali vergullar (` ; `) shart emas. Har qanday amal yoki operator aslida obyektning metodidir. Masalan:
```ruby
5.times { puts "Salom, Khorazmiy AI!" }
```
Bu yerda `5` oddiy son emas, balki `Integer` sinfining to'laqonli obyektidir va uning `times` nomli metodi chaqirilmoqda.

---

## 2. Virtual Mashina Arxitekturasi: YARV, Baytkod va YJIT

Ruby manba kodi (`.rb`) to'g'ridan-to'g'ri operatsion tizimda ishlamaydi. U zamonaviy virtual mashinalar vositasida ijro etiladi.

### 2.1. YARV (Yet Another Ruby VM)
Ruby 1.9 versiyasidan boshlab rasmiy MRI (CRuby) Koichi Sasada tomonidan yaratilgan **YARV** stekka asoslangan virtual mashinasidan foydalanadi.
1. **Parser & Lexer:** Ripper va Bison orqali kod AST (Abstract Syntax Tree)ga o'giriladi.
2. **Bytecode Compiler:** AST YARV baytkod ko'rsatmalariga (InstructionSequence) kompilyatsiya qilinadi.
3. **VM Execution Loop:** YARV steki orqali ko'rsatmalar bajariladi.

### 2.2. YJIT (Yet Another Just-In-Time Compiler)
Ruby 3.1 da Shopify muhandislari tomonidan taqdim etilgan va Ruby 3.2/3.3 da Rust tilida qayta yozilgan **YJIT** Ruby ekotizimida inqilob qildi:
- **Basic Block Versioning (BBV):** YJIT butun metodni birdaniga kompilyatsiya qilmaydi, balki ko'p takrorlanadigan asosiy bloklarni aniqlab, ularni bevosita x86_64 yoki ARM64 mashina kodiga aylantiradi.
- **Rails uchun 20-40% tezlashuv:** Rails kabi murakkab va dinamik tizimlarda YJIT xotira sarfini me'yorda saqlagan holda veb-so'rovlarni tezkor qayta ishlashni ta'minlaydi (`ruby --yjit server.rb`).

---

## 3. Mukammal Obyekt Modeli: "Hamma narsa Obyekt"

Ruby-da ibtidoiy (primitive) tushuncha umuman mavjud emas. `nil`, `true`, `false`, hatto sinflarning o'zi ham obyekt hisoblanadi.

```
                  +-------------------+
                  |    BasicObject    |
                  +-------------------+
                            |
                  +-------------------+
                  |      Object       |
                  +-------------------+
                   /        |                          /         |                  +---------+  +-----------+  +---------+
         | Numeric |  |  String   |  | Module  |
         +---------+  +-----------+  +---------+
              |                           |
         +---------+                 +---------+
         | Integer |                 |  Class  |
         +---------+                 +---------+
```

### 3.1. Eigenclass (Singleton Class)
Har bir obyekt o'ziga xos individual metodlarga ega bo'lishi mumkin. Ruby buni obyekt va uning sinfi orasiga yashirin **Eigenclass** (metasinf) qistirish orqali amalga oshiradi:
```ruby
matn = "Salom"
def matn.maxsus_salom
  "Faqat ushbu nusxa uchun maxsus metod!"
end
```

### 3.2. Metod Qidirish Yo'li (Ancestors Lookup Path)
Ruby-da metod chaqirilganda, virtual mashina quyidagi zanjir bo'ylab qidiradi:
1. Obyektning Eigenclass-i
2. Joriy sinf (Class)
3. Sinfga kiritilgan modullar (Prepended modules, keyin Included modules)
4. Ota sinf (Superclass)
5. `Object` -> `Kernel` -> `BasicObject`
6. Agar topilmasa: `method_missing` zanjiri ishga tushadi.

---

## 4. Xotira Boshqaruvi va Garbage Collection (GC)

Ruby dinamik til bo'lgani uchun xotira dasturchi tomonidan qo'lda tozalanmaydi, uni maxsus **Garbage Collector** boshqaradi.

### 4.1. Generational GC (RGenGC)
Ruby 2.1 dan boshlab avlodlarga asoslangan GC ishlaydi:
- **Young Generation:** Yangi yaratilgan obyektlar tezda sinovdan o'tadi. Obyektlarning 90% bir necha soniyada yaroqsiz bo'ladi (ephemeral).
- **Old Generation:** Bir necha tozalash siklidan omon qolgan obyektlar keksalar toifasiga o'tkaziladi va ularni tekshirish chastotasi kamaytiriladi.

### 4.2. Compact GC va Xotira Fragmentatsiyasi
Ruby 2.7 va 3.0 dan boshlab xotiradagi bo'shliqlarni siqish (Compacting GC) joriy etildi: `GC.compact`. Bu uzoq vaqt ishlaydigan veb-serverlarda RAM sarfini 20-30% ga tejaydi.

---

## 5. Bloklar, Procs, Lambdalar va Funksional Imkoniyatlar

Ruby o'zining kod bloklari (`do ... end` va `{ ... }`) bilan boshqa tillardan yaqqol ajralib turadi.

### 5.1. Farqlar: Proc vs Lambda
| Xususiyat | Proc (`Proc.new`) | Lambda (`lambda` yoki `->`) |
|---|---|---|
| Argumentlar soni | Moslashuvchan (ortiqcha tashlab yuboriladi, yetmagani `nil`) | Qat'iy (`ArgumentError` beradi) |
| `return` xatti-harakati | O'rab turgan tashqi metoddan chiqib ketadi | Faqat lambdaning o'zidan qiymat qaytaradi |

### 5.2. Symbol#to_proc sehri
```ruby
foydalanuvchilar.map(&:name)
# Ushbu sintaksis quyidagining ekvivalenti:
# foydalanuvchilar.map { |f| f.name }
```

---

## 6. Metaprogramming va Domain-Specific Languages (DSL)

Ruby metaprogramming (kod yozuvchi kod) bo'yicha dunyodagi eng moslashuvchan tillardan biridir. Rake, RSpec, Rails marshrutlash tizimi barchasi Ruby DSL asosiga qurilgan.

### 6.1. Asosiy Metaprogramming Asboblari:
- `define_method`: Ish vaqtida dinamik metodlar yaratish.
- `method_missing`: Obyektda yo'q metod chaqirilganda uni ilg'ab olish (ActiveRecord-ning `find_by_email` kabi dinamik qidiruvlari shu asosda).
- `instance_eval` va `class_eval`: Kod kontekstini va ko'rinish chegaralarini o'zgartirish.

---

## 7. Ruby on Rails: Zamonaviy Veb Startaplar Qiroli

David Heinemeier Hansson (DHH) tomonidan yaratilgan Ruby on Rails (RoR) quyidagi tamoyillarga tayanadi:
1. **Convention over Configuration (Sozlashdan ko'ra kelishuv afzal):** Dasturchi har bir jadval nomi yoki yo'lni qo'lda belgilamaydi, umumiy qoidalarga rioya qiladi (`Post` modeli `posts` jadvaliga ulanadi).
2. **Don't Repeat Yourself (DRY):** Har bir bilim tizimda faqat bir marta yoziladi.
3. **The Asset Pipeline va Hotwire:** Zamonaviy Rails 7/8 murakkab Node.js/Webpack buildsiz, bevosita brauzer standartlari (Importmaps, Turbo Streams, Stimulus) orqali yashin tezligida reaktiv interfeys yaratish imkonini beradi.

---

## 8. Konkurentlik va Parallelizm: GVL, Fibers va Ractor

Ruby 3.0 ning eng ulkan va'dasi "Ruby 3x3" (Ruby 2.0 dan 3 baravar tezroq bo'lish) va parallelizm edi.

### 8.1. GVL (Global VM Lock)
MRI-da bitta Ruby jarayonida bir vaqtning o'zida faqat bitta OS thread C-kodini bajarishi mumkin. Bu I/O operatsiyalarida to'sqinlik qilmaydi, ammo CPU-bound ishlarda to'liq parallelizm bermaydi.

### 8.2. Ractor (Ruby Actor Model)
Ractor-lar bir-birlari bilan xotirani bo'lishmaydi (Shared-nothing architecture). Ular xabarlar almashish (`send` / `take`) orqali bir nechta CPU yadrolarida GVL-siz to'liq parallel ishlaydi.

### 8.3. Fibers va Asinxron I/O
Yengil vaznli korutinalar (Fibers) Falcon kabi asinxron serverlarga bitta jarayonda o'n minglab WebSockets ulanishlarni boshqarishga imkon beradi.

---

## 9. Korxona Darajasidagi Xavfsizlik va Unumdorlik

Rails xavfsizlik bo'yicha dunyoda standart o'rnatgan freymvorkdir:
- **SQL Injection:** ActiveRecord barcha parametrlarni tayyorlangan iboralar (Parameterized Statements) orqali avtomatik tozalaydi.
- **CSRF Himoyasi:** Har bir POST/PUT so'rovi `authenticity_token` bilan himoyalanadi.
- **XSS Himoyasi:** ERB shablonlari chiqayotgan matnlarni avtomatik `h()` orqali ekranlashtiradi (HTML Escaping).

---

## 10. Sun'iy Intellekt Davrida Ruby va Startap Arxitekturasi

Bugungi kunda GitHub, Shopify, Airbnb, GitLab va Stripe kabi gigantlar Ruby va Rails asosida kuniga milliardlab dollarlik tranzaksiyalarni amalga oshirmoqda.

AI davrida Rails eng yaxshi "AI Wrapper" va mahsulot ishlab chiqish vositasiga aylandi:
- Yangi startap g'oyasini 1-2 hafta ichida tayyor MVP (Minimum Viable Product)ga aylantirish.
- OpenAI, Anthropic, Gemini API-larini ActiveJob va Background Worker (Sidekiq) orqali integratsiya qilish.
- Turbo Streams orqali LLM javoblarini foydalanuvchi ekraniga real vaqtda striming qilish (Token Streaming).

Ushbu 1000 ta topshiriqdan iborat mukammal amaliy to'plam sizni Ruby tili sintaksisidan boshlab eng yuqori darajadagi dasturiy ta'minot arxitektorligigacha yetaklaydi.
