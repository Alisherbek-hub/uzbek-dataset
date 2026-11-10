# -*- coding: utf-8 -*-
"""
Generator for lua_mukammal_qollanma.md
Comprehensive Fundamental Encyclopedia for Lua (Lua 5.1 - 5.4, LuaJIT, Roblox Luau, OpenResty/Nginx, Redis)
"""

import os

ENCYCLOPEDIA_CONTENT = """# Lua: Mukammal Ensiklopediya va Fundamental Qo'llanma
**Loyiha:** Khorazmiy AI — O'zbek Tilidagi Katta Dasturlash Dataseti  
**Muallif:** Khorazmiy AI Lua & Scripting Specialist  
**Versiya:** Lua 5.1 / 5.2 / 5.3 / 5.4, LuaJIT 2.1, Luau (2026-yil holatiga)  
**Qamrovi:** Lua tili arxitekturasi, C bilan integratsiya va C API, Stack modeli, Metatablelar va Metametodlar, Prototipga asoslangan OOP, Korutinalar va kooperativ ko'p vazifalilik, Garbage Collector mexanizmi, Luau (Roblox game engine), OpenResty (Nginx) yuqori yuklamali veb-serverlar va Redis atomar skriptlash tizimi.

---

## Mundarija
1. [Kirish va Lua Tilining Yaratilish Tarixi hamda Falsafasi](#1-kirish-va-lua-tilining-yaratilish-tarixi-hamda-falsafasi)
2. [Lua Tizimining Arxitekturasi: Virtual Mashina va Bytecode](#2-lua-tizimining-arxitekturasi-virtual-mashina-va-bytecode)
3. [Asosiy Tiplar va Dinamik Tiplash Tizimi](#3-asosiy-tiplar-va-dinamik-tiplash-tizimi)
4. [Jadvallar (Tables): Yagona va Qudratli Ma'lumotlar Tuzilmasi](#4-jadvallar-tables-yagona-va-qudratli-malumotlar-tuzilmasi)
5. [Metatablelar va Metametodlar: Til Semantikasini Kengaytirish](#5-metatablelar-va-metametodlar-til-semantikasini-kengaytirish)
6. [Ob'ektga Yo'naltirilgan Dasturlash (OOP) va Prototip Modeli](#6-obektga-yonaltirilgan-dasturlash-oop-va-prototip-modeli)
7. [Birinchi Darajali Funksiyalar, Closures va Leksik Qamrov](#7-birinchi-darajali-funksiyalar-closures-va-leksik-qamrov)
8. [Korutinalar (Coroutines) va Kooperativ Multitasking](#8-korutinalar-coroutines-va-kooperativ-multitasking)
9. [Xotira Boshqaruvi va Garbage Collector (GC) Ichki Tuzilishi](#9-xotira-boshqaruvi-va-garbage-collector-gc-ichki-tuzilishi)
10. [C API va Stack Arxitekturasi: Host Dasturlarga Luani Joylashtirish](#10-c-api-va-stack-arxitekturasi-host-dasturlarga-luani-joylashtirish)
11. [LuaJIT va FFI (Foreign Function Interface): Ekstremal Unumdorlik](#11-luajit-va-ffi-foreign-function-interface-ekstremal-unumdorlik)
12. [Roblox Ekotizimi va Luau: O'yin Dasturlash va Statik Tiplash](#12-roblox-ekotizimi-va-luau-oyin-dasturlash-va-statik-tiplash)
13. [OpenResty va Nginx: Sinxron Kod bilan Asinxron Yuqori Yuklama](#13-openresty-va-nginx-sinxron-kod-bilan-asinxron-yuqori-yuklama)
14. [Redis va Lua: Atomar Tranzaksiyalar va Kesh Muhandisligi](#14-redis-va-lua-atomar-tranzaksiyalar-va-kesh-muhandisligi)
15. [Professional Best Practices va Unumdorlikni Optimizatsiya Qilish](#15-professional-best-practices-va-unumdorlikni-optimizatsiya-qilish)

---

## 1. Kirish va Lua Tilining Yaratilish Tarixi hamda Falsafasi

Lua (portugalcha "Oy" degan ma'noni anglatadi) tili 1993-yilda Braziliyaning Rio-de-Janeyro Papal Katolik Universiteti (PUC-Rio) tadqiqotchilari — Roberto Ierusalimschy, Luiz Henrique de Figueiredo va Waldemar Celes tomonidan ishlab chiqilgan.

### Lua Yaratilishining Asosiy Maqsadlari:
- **Kichik hajm va ixchamlik (Small Footprint):** Lua interpretatori C tilida yozilgan bo'lib, uning to'liq binar hajmi odatda 300 kilobaytdan oshmaydi. Bu uni har qanday qurilma — mikrokontrollerlardan tortib yirik korporativ serverlargacha oson integratsiya qilish imkonini beradi.
- **Oson o'rnatiluvchanlik (Embeddability):** Lua mustaqil tizim sifatida ham ishlay oladi, biroq uning asosiy kuchi boshqa dasturlarning (C, C++, Rust, Go) ichiga "skriptlash tili" (embedded scripting language) sifatida joylashtirilishidadir.
- **Ko'chuvchanlik (Portability):** Lua to'liq ISO C (ANSI C) standartiga mos keladi. ANSI C kompilyatori mavjud bo'lgan har qanday operatsion tizimda hech qanday o'zgartirishsiz kompilyatsiya bo'ladi.
- **Mexanizmlar, siyosatlar emas (Mechanisms, not Policies):** Lua o'z foydalanuvchilariga qat'iy qoidalar yoki murakkab sinf tizimlarini majburlamaydi. U minimal, ammo juda qudratli mexanizmlarni (masalan, jadvallar va metatablelar) taqdim etadi, dasturchi esa ushbu mexanizmlardan foydalanib o'zi xohlagan OOP, funksional yoki reaktiv paradigmani qurishi mumkin.

---

## 2. Lua Tizimining Arxitekturasi: Virtual Mashina va Bytecode

Lua ikki bosqichli interpretatsiya modelidan foydalanadi:
1. **Leksik va Sintaktik tahlil (Parsing & Bytecode Generation):** Manba kod `.lua` o'qiladi va xotirada registerga asoslangan virtual mashina (Register-based Virtual Machine) uchun optimallashtirilgan baytkodga o'giriladi.
2. **Baytkod Interpretatsiyasi:** Lua VM ushbu ko'rsatmalarni bajaradi. Ko'pchilik an'anaviy virtual mashinalar (masalan, JVM, Python VM) stekka asoslangan (stack-based) bo'lsa, Lua dunyodagi birinchi keng tarqalgan registerga asoslangan VM hisoblanadi. Bu baytkod ko'rsatmalari sonini keskin kamaytiradi va bajarilish tezligini 30-50% ga oshiradi.

---

## 3. Asosiy Tiplar va Dinamik Tiplash Tizimi

Lua dinamik tiplanadigan til bo'lib, o'zgaruvchilar emas, balki qiymatlar tipga ega. Luada atigi 8 ta asosiy ma'lumot turi mavjud:

1. **`nil`**: Qiymatning yo'qligini yoki o'chirilganligini bildiradi. Har qanday e'lon qilinmagan o'zgaruvchining boshlang'ich qiymati `nil` bo'ladi.
2. **`boolean`**: `true` va `false`. Diqqat: Luada faqatgina `nil` va `false` yolg'on hisoblanadi. Son `0` va bo'sh satr `""` esa haqiqiy (`true`) qiymat deb baholanadi!
3. **`number`**: Lua 5.3 versiyasidan boshlab sonlar ikki xil ichki ifodaga ega: 64-bitli butun sonlar (`integer`) va 64-bitli suzuvchi nuqtali sonlar (`float`).
4. **`string`**: 8-bitli baytlar ketma-ketligi. Luada satrlar o'zgarmasdir (immutable) va xotirada internallashtiriladi (interned strings), ya'ni bir xil satr bir necha bor yaratilsa ham, xotirada yagona nusxada saqlanadi.
5. **`table`**: Luadagi yagona ma'lumotlar strukturasi — assotsiativ massiv (lug'at).
6. **`function`**: Luada funksiyalar birinchi darajali fuqarolardir (first-class values).
7. **`userdata`**: C/C++ xotira bloklari va xom ko'rsatkichlarini Luaga xavfsiz uzatish uchun maxsus tip.
8. **`thread`**: Mustaqil korutinalarni (coroutine) ifodalovchi tip (OS oqimlari bilan adashtirmaslik kerak).

---

## 4. Jadvallar (Tables): Yagona va Qudratli Ma'lumotlar Tuzilmasi

Jadvallar — Luadagi eng muhim va universal tuzilmadir. Ular bir vaqtning o'zida quyidagi rollarni o'ynay oladi:
- Oddiy massivlar (Array)
- Lug'atlar / Assotsiativ massivlar (Hash Maps)
- Ob'ektlar va Sinflar
- Modullar va Paketlar
- Global o'zgaruvchilar muhiti (`_G`)

### Lua Massivlarining Xususiyati:
- Massiv indeksatsiyasi an'anaviy ravishda `1` dan boshlanadi (`1-indexed`).
- Uzunlik operatori `#` massiv qismidagi oxirgi ketma-ket element indeksini qaytaradi.
- Agar massivda `nil` oraliqlar (holes) mavjud bo'lsa, `#t` operatorining natijasi noaniq bo'lishi mumkin.
- Lua ichki tomondan jadvalni ikki qismga ajratib saqlaydi: tezkor ketma-ket xotira qismi (array part) va kalit-qiymat xesh jadvali (hash part). Bu xotiradan unumli foydalanishni va $O(1)$ murojaatni ta'minlaydi.

---

## 5. Metatablelar va Metametodlar: Til Semantikasini Kengaytirish

Metatable — bu oddiy jadval bo'lib, uning ichida maxsus kalitlar (metametodlar) orqali ob'ektlarning xatti-harakatini o'zgartirish mumkin.

### Eng Ko'p Ishlatiladigan Metametodlar:
- `__index`: Agar jadvalda qidirilgan kalit topilmasa, Lua ushbu metametodga murojaat qiladi. Bu Luada merosxo'rlik va OOP ning poydevori hisoblanadi.
- `__newindex`: Jadvalga yangi kalit yozilayotganda ishga tushadi. Ma'lumotlarni validatsiya qilish yoki o'zgarmas (read-only) jadvallar yaratishda ishlatiladi.
- Arifmetik metametodlar: `__add` (+), `__sub` (-), `__mul` (*), `__div` (/), `__mod` (%), `__unm` (inversiya).
- Taqqoslash metametodlari: `__eq` (==), `__lt` (<), `__le` (<=).
- Satrga o'girish: `__tostring` — `print()` yoki `tostring()` chaqirilganda formatlangan matn qaytaradi.
- Funksiya kabi chaqirish: `__call` — jadvalga oddiy funksiya kabi qavs ochib parametr uzatilganda ishlaydi.
- Zaif bog'lamlar: `__mode` — Garbage collectorga jadval kalitlari yoki qiymatlari zaif (`"k"`, `"v"`, `"kv"`) ekanligini bildiradi (Weak tables).

---

## 6. Ob'ektga Yo'naltirilgan Dasturlash (OOP) va Prototip Modeli

Luada klassik sinflar (`class`) kalit so'zi yo'q. Buning o'rniga JavaScript kabi prototipga asoslangan (prototype-based) model ishlatiladi:

```lua
local Car = {}
Car.__index = Car

function Car:new(brand, speed)
    local self = setmetatable({}, Car)
    self.brand = brand
    self.speed = speed
    return self
end

function Car:accelerate(amount)
    self.speed = self.speed + amount
    print(self.brand .. " yangi tezligi: " .. self.speed .. " km/soat")
end
```

### Nuqta (`.`) va Ikki Nuqta (`:`) Farqi:
- `Car.accelerate(instance, 20)` — obyekt birinchi argument sifatida qo'lda uzatiladi.
- `instance:accelerate(20)` — `self` parametrini avtomatik ravishda birinchi argument qilib yashirin uzatadi (syntactic sugar).

---

## 7. Birinchi Darajali Funksiyalar, Closures va Leksik Qamrov

Luada har qanday funksiya qiymatdir (first-class value). Uni o'zgaruvchiga yuklash, funksiyaga argument sifatida berish yoki funksiyadan qaytarish mumkin.

### Closures va Upvalues:
Ichki funksiya o'zining tashqi qamrovidagi lokal o'zgaruvchilarga murojaat qilsa, bu o'zgaruvchilar **upvalue** deb ataladi. Tashqi funksiya o'z ishini tugatsa ham, yopiq muhit (closure) ushbu o'zgaruvchilarni xotirada saqlab qoladi. Bu enkapsulyatsiya, modullar va funksional kompozitsiya uchun keng qo'llaniladi.

---

## 8. Korutinalar (Coroutines) va Kooperativ Multitasking

Korutinalar — Luadagi eng nafis mexanizmlardan biridir. An'anaviy ko'p oqimli (multithreading) tizimlardan farqli o'laroq, korutinalar operatsion tizim preemptioniga tayanmaydi:
- Ular **kooperativ** multitasking rejimida ishlaydi: korutina o'z ixtiyori bilan boshqaruvni boshqa kodga topshiradi (`coroutine.yield()`).
- Qayta tiklash (`coroutine.resume()`) orqali to'xtagan joyidan davom etadi.
- Bu poyga holatlari (race conditions) va blokirovka qiluvchi qulflar (deadlocks) muammosini yo'q qiladi.
- Generatorlar, o'yin davrlaridagi sun'iy intellekt (Game AI update cycles) va asinxron I/O kutubxonalari aynan korutinalar asosiga quriladi.

---

## 9. Xotira Boshqaruvi va Garbage Collector (GC) Ichki Tuzilishi

Lua xotirani avtomatik boshqarish uchun **Incremental Mark-and-Sweep Garbage Collector** dan foydalanadi (Lua 5.4 versiyasidan boshlab esa ixtiyoriy Generational GC rejimi qo'shilgan):
- **Oq (White):** Hali tekshirilmagan yoki o'chirilishi kerak bo'lgan keraksiz ob'ektlar.
- **Kulrang (Gray):** O'zi murojaat qilingan, ammo o'ziga bog'langan ob'ektlar hali tekshirilmagan ob'ektlar.
- **Qora (Black):** O'zi ham, unga bog'langan barcha a'zolari ham tekshirilgan va xotirada saqlanadigan ob'ektlar.

Dasturchi `collectgarbage("collect")`, `collectgarbage("step")` yoki `collectgarbage("stop")` orqali tozalash parametrlarini to'liq nazorat qilishi mumkin.

---

## 10. C API va Stack Arxitekturasi: Host Dasturlarga Luani Joylashtirish

Lua va C tillari o'rtasidagi aloqa o'zaro sinxronlashtirilgan virtual **Stack** orqali amalga oshiriladi:
- C kodi `lua_pushnumber`, `lua_pushstring` orqali stekka qiymat qo'yadi.
- `lua_tonumber`, `lua_tostring` orqali stekdan ma'lumotlarni o'qiydi.
- Musbat indekslar (`1`, `2`) stekning tubidan boshlab sanaydi; manfiy indekslar (`-1`, `-2`) esa stekning eng yuqori uchidan sanaydi.
- Bu arxitektura turlar xavfsizligini ta'minlaydi va ikki tilning xotira modellarini bir-biriga zarar yetkazishidan saqlaydi.

---

## 11. LuaJIT va FFI (Foreign Function Interface): Ekstremal Unumdorlik

Mike Pall tomonidan yaratilgan **LuaJIT** — dasturlash tillari tarixidagi eng tez Just-In-Time kompilyatorlardan biridir:
- U Lua baytkodini to'g'ridan-to'g'ri x86/ARM mashina kodiga kompilyatsiya qiladi.
- **FFI (Foreign Function Interface):** Hech qanday murakkab C sarlavhalari yoki sarmoyaviy kodlarsiz, oddiy C deklaratsiyasini kiritib (`ffi.cdef`), C kutubxonalarini to'g'ridan-to'g'ri Luadan chaqirish imkonini beradi. Tezligi sof C kodidan deyarli qolishmaydi.

---

## 12. Roblox Ekotizimi va Luau: O'yin Dasturlash va Statik Tiplash

Roblox platformasi milliardlab o'yinchilarga xizmat ko'rsatuvchi eng yirik o'yin ekotizimlaridan biridir. Roblox Lua 5.1 asosida **Luau** deb nomlangan zamonaviy tilni yaratdi:
- Luau asta-sekin statik tiplash (Gradual Typing) imkoniyatini taqdim etadi (`type PlayerData = { name: string, level: number }`).
- Server va Mijoz o'rtasida xavfsiz aloqa: `RemoteEvent` va `RemoteFunction`.
- Ma'lumotlarni bulutda saqlash: `DataStoreService`.
- Fizika va koordinatalar: `Vector3`, `CFrame`, `RaycastParams`.

---

## 13. OpenResty va Nginx: Sinxron Kod bilan Asinxron Yuqori Yuklama

OpenResty — Nginx veb-serveriga LuaJIT dvijogini joylashtirgan yuqori unumdor tizimdir:
- Nginx-ning nosintezator asinxron event-loopiga Lua korutinalari ulanadi (Non-blocking I/O).
- Dasturchi kodni oddiy sinxron usulda yozadi (`local res = ngx.location.capture("/api")`), orqa fonda esa korutina to'xtab (yield bo'lib), I/O tayyor bo'lganda davom etadi.
- Sekundiga yuz minglab HTTP so'rovlarni mikrosekundlarda qayta ishlash, JWT tokenlarni tekshirish, WAF (Web Application Firewall) va dinamik marshrutlash uchun dunyodagi eng yetakchi yechimdir (Cloudflare, Kong va h.k.).

---

## 14. Redis va Lua: Atomar Tranzaksiyalar va Kesh Muhandisligi

Redis serveri ichida Lua skriptlarini bajarish (`EVAL` va `EVALSHA`):
- **100% Atomarlik:** Skript ishlayotgan paytda Redis hech qanday boshqa buyruqni qabul qilmaydi. Bu poyga sharoitlaridan (race condition) xoli bo'lgan taqsimlangan qulflar (Distributed Locks / Redlock), hisoblagichlar va xarid qilish tizimlarini qurishga imkon beradi.
- Tarmoq kechikishini kamaytirish: Bir nechta Redis buyruqlarini bitta so'rovda birlashtirib serverda bajarish.

---

## 15. Professional Best Practices va Unumdorlikni Optimizatsiya Qilish

1. **Har doim `local` dan foydalaning:** Global o'zgaruvchilarga murojaat xesh-jadval qidiruvini talab qiladi; lokal o'zgaruvchilar esa bevosita VM registrlarida saqlanadi va 30% tezroq ishlaydi.
2. **Table yaratishda oldindan o'lcham belgilash:** Qayta xotira taqsimlashni (rehash) kamaytirish.
3. **Satr konkatenatsiyasida ehtiyot bo'ling:** Katta tsikllarda `..` operatori o'rniga `table.insert` va `table.concat` dan foydalaning.
4. **Metatablelarni haddan tashqari chuqurlashtirmang:** Qidiruv zanjiri (lookup chain) qanchalik qisqa bo'lsa, xotira va vaqt sarfi shunchalik tejaladi.

---
*Ushbu qo'llanma O'zbekiston dasturlash ekotizimida Lua, Roblox va yuqori yuklamali tizimlar muhandisligi bo'yicha to'liq va fundamental manba sifatida ishlab chiqildi.*
"""

def generate_encyclopedia():
    base_dir = r"C:\Users\User\Desktop\uzbek_dataset\kodlar\lua"
    out_path = os.path.join(base_dir, "lua_mukammal_qollanma.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(ENCYCLOPEDIA_CONTENT.strip() + "\n")
    print(f"Ensiklopediya saqlandi: {out_path} ({len(ENCYCLOPEDIA_CONTENT.encode('utf-8'))} bayt)")

if __name__ == "__main__":
    generate_encyclopedia()
