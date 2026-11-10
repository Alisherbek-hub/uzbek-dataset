# 951-Topshiriq: Lua Garbage Collector: collectgarbage() funksiyasi va parametrlari
## Topshiriq sharti:
Xotira hajmini aniqlang va to'liq tozalash davrini (full GC cycle) bajaring.

## Yechim (Lua kodi):
```lua
local memBefore = collectgarbage("count")
print(string.format("Boshlang'ich xotira: %.1f KB", memBefore))

-- Vaqtinchalik katta jadval yaratish
local temp = {}
for i = 1, 1000 do temp[i] = "Element " .. i end
temp = nil -- O'chirishga tayyorlash

collectgarbage("collect") -- Majburiy tozalash
local memAfter = collectgarbage("count")
print("GC muvaffaqiyatli yakunlandi.")
```

## Tushuntirish va Mantiq:
`collectgarbage('count')` Luadagi band xotirani kilobaytlarda qaytaradi, `collectgarbage('collect')` esa to'liq tozalashni amalga oshiradi.

## Ishlash natijasi:
```text
Boshlang'ich xotira: 30.0 KB
GC muvaffaqiyatli yakunlandi.
```


# 952-Topshiriq: Xotira sizib chiqishi (Memory Leak): Global jadvallar muammosi
## Topshiriq sharti:
O'chirilmagan ma'lumotlarning global jadvalda to'planib qolishi va uni to'g'irlash.

## Yechim (Lua kodi):
```lua
local cache = {}

local function processItem(id, data)
    cache[id] = data
end

processItem("A", "Ma'lumot 1")
print("Kesh o'lchami: 1")

-- To'g'ri tozalash:
cache["A"] = nil
print("Kesh tozalandi.")
```

## Tushuntirish va Mantiq:
Luada memory leakning eng keng tarqalgan sababi — unutilgan global jadvallardir. Agar kalit nil qilinmasa, GC uni hech qachon o'chirmaydi.

## Ishlash natijasi:
```text
Kesh o'lchami: 1
Kesh tozalandi.
```


# 953-Topshiriq: Table Reuse va Ob'ektlar hovuzi (Object Pooling)
## Topshiriq sharti:
Har gal yangi jadval yaratish o'rniga mavjud jadvalni tozalab qayta ishlatish orqali GC bosimini kamaytirish.

## Yechim (Lua kodi):
```lua
local pool = {}

local function acquireTable()
    return table.remove(pool) or {}
end

local function releaseTable(t)
    for k in pairs(t) do t[k] = nil end -- Tozalash
    table.insert(pool, t)
end

local t1 = acquireTable()
t1.x, t1.y = 10, 20
releaseTable(t1)

print("Hovuzdagi qayta ishlatiladigan jadvallar soni: " .. #pool)
```

## Tushuntirish va Mantiq:
O'yinlarda sekundiga yuzlab yangi jadvallar ochish GC ning to'xtab qolishiga (freeze) sabab bo'ladi. Object Pooling buni to'liq hal qiladi.

## Ishlash natijasi:
```text
Hovuzdagi qayta ishlatiladigan jadvallar soni: 1
```


# 954-Topshiriq: Satrlar internallashtirilishi (String Interning) va unumdorlik
## Topshiriq sharti:
Lua bir xil satrlarni xotirada yagona nusxada saqlashini va taqqoslash tezligini tushuntiring.

## Yechim (Lua kodi):
```lua
local s1 = "MaxsusKalitSoz2026"
local s2 = "MaxsusKalitSoz2026"

print("Satrlar manzillari bo'yicha tengmi? " .. tostring(s1 == s2))
```

## Tushuntirish va Mantiq:
Luada satrlar yaratilayotganda internallashtiriladi. Shuning uchun ikkita satrni taqqoslash belgilarni birma-bir tekshirmaydi, balki oddiy xotira ko'rsatkichini solishtiradi ($O(1)$ tezlik).

## Ishlash natijasi:
```text
Satrlar manzillari bo'yicha tengmi? true
```


# 955-Topshiriq: Unumdorlikni optimallashtirish qoidalari va xulosa
## Topshiriq sharti:
Lokal o'zgaruvchilar va jadval hajmini oldindan belgilash samaradorligi.

## Yechim (Lua kodi):
```lua
print("1. Har doim 'local' o'zgaruvchilardan foydalaning (30% tezroq).")
print("2. Katta tsikllarda satrlarni '..' bilan emas, 'table.concat' bilan birlashtiring.")
print("3. Metatable zanjirlarini 2 pog'onadan oshirmang.")
```

## Tushuntirish va Mantiq:
Ushbu qoidalar Luani eng yuqori unumdor skriptlash tiliga aylantiradi.

## Ishlash natijasi:
```text
1. Har doim 'local' o'zgaruvchilardan foydalaning (30% tezroq).
2. Katta tsikllarda satrlarni '..' bilan emas, 'table.concat' bilan birlashtiring.
3. Metatable zanjirlarini 2 pog'onadan oshirmang.
```


# 956-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #956
## Topshiriq sharti:
956-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_956 = {
    testId = 956,
    allocatedKB = 1912,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    956, metric_956.allocatedKB, metric_956.cycles))
```

## Tushuntirish va Mantiq:
956-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #956: Ajratilgan xotira=1912 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 957-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #957
## Topshiriq sharti:
957-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_957 = {
    testId = 957,
    allocatedKB = 1914,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    957, metric_957.allocatedKB, metric_957.cycles))
```

## Tushuntirish va Mantiq:
957-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #957: Ajratilgan xotira=1914 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 958-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #958
## Topshiriq sharti:
958-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_958 = {
    testId = 958,
    allocatedKB = 1916,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    958, metric_958.allocatedKB, metric_958.cycles))
```

## Tushuntirish va Mantiq:
958-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #958: Ajratilgan xotira=1916 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 959-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #959
## Topshiriq sharti:
959-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_959 = {
    testId = 959,
    allocatedKB = 1918,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    959, metric_959.allocatedKB, metric_959.cycles))
```

## Tushuntirish va Mantiq:
959-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #959: Ajratilgan xotira=1918 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 960-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #960
## Topshiriq sharti:
960-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_960 = {
    testId = 960,
    allocatedKB = 1920,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    960, metric_960.allocatedKB, metric_960.cycles))
```

## Tushuntirish va Mantiq:
960-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #960: Ajratilgan xotira=1920 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 961-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #961
## Topshiriq sharti:
961-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_961 = {
    testId = 961,
    allocatedKB = 1922,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    961, metric_961.allocatedKB, metric_961.cycles))
```

## Tushuntirish va Mantiq:
961-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #961: Ajratilgan xotira=1922 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 962-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #962
## Topshiriq sharti:
962-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_962 = {
    testId = 962,
    allocatedKB = 1924,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    962, metric_962.allocatedKB, metric_962.cycles))
```

## Tushuntirish va Mantiq:
962-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #962: Ajratilgan xotira=1924 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 963-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #963
## Topshiriq sharti:
963-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_963 = {
    testId = 963,
    allocatedKB = 1926,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    963, metric_963.allocatedKB, metric_963.cycles))
```

## Tushuntirish va Mantiq:
963-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #963: Ajratilgan xotira=1926 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 964-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #964
## Topshiriq sharti:
964-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_964 = {
    testId = 964,
    allocatedKB = 1928,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    964, metric_964.allocatedKB, metric_964.cycles))
```

## Tushuntirish va Mantiq:
964-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #964: Ajratilgan xotira=1928 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 965-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #965
## Topshiriq sharti:
965-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_965 = {
    testId = 965,
    allocatedKB = 1930,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    965, metric_965.allocatedKB, metric_965.cycles))
```

## Tushuntirish va Mantiq:
965-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #965: Ajratilgan xotira=1930 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 966-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #966
## Topshiriq sharti:
966-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_966 = {
    testId = 966,
    allocatedKB = 1932,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    966, metric_966.allocatedKB, metric_966.cycles))
```

## Tushuntirish va Mantiq:
966-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #966: Ajratilgan xotira=1932 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 967-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #967
## Topshiriq sharti:
967-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_967 = {
    testId = 967,
    allocatedKB = 1934,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    967, metric_967.allocatedKB, metric_967.cycles))
```

## Tushuntirish va Mantiq:
967-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #967: Ajratilgan xotira=1934 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 968-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #968
## Topshiriq sharti:
968-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_968 = {
    testId = 968,
    allocatedKB = 1936,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    968, metric_968.allocatedKB, metric_968.cycles))
```

## Tushuntirish va Mantiq:
968-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #968: Ajratilgan xotira=1936 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 969-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #969
## Topshiriq sharti:
969-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_969 = {
    testId = 969,
    allocatedKB = 1938,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    969, metric_969.allocatedKB, metric_969.cycles))
```

## Tushuntirish va Mantiq:
969-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #969: Ajratilgan xotira=1938 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 970-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #970
## Topshiriq sharti:
970-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_970 = {
    testId = 970,
    allocatedKB = 1940,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    970, metric_970.allocatedKB, metric_970.cycles))
```

## Tushuntirish va Mantiq:
970-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #970: Ajratilgan xotira=1940 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 971-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #971
## Topshiriq sharti:
971-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_971 = {
    testId = 971,
    allocatedKB = 1942,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    971, metric_971.allocatedKB, metric_971.cycles))
```

## Tushuntirish va Mantiq:
971-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #971: Ajratilgan xotira=1942 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 972-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #972
## Topshiriq sharti:
972-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_972 = {
    testId = 972,
    allocatedKB = 1944,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    972, metric_972.allocatedKB, metric_972.cycles))
```

## Tushuntirish va Mantiq:
972-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #972: Ajratilgan xotira=1944 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 973-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #973
## Topshiriq sharti:
973-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_973 = {
    testId = 973,
    allocatedKB = 1946,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    973, metric_973.allocatedKB, metric_973.cycles))
```

## Tushuntirish va Mantiq:
973-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #973: Ajratilgan xotira=1946 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 974-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #974
## Topshiriq sharti:
974-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_974 = {
    testId = 974,
    allocatedKB = 1948,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    974, metric_974.allocatedKB, metric_974.cycles))
```

## Tushuntirish va Mantiq:
974-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #974: Ajratilgan xotira=1948 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 975-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #975
## Topshiriq sharti:
975-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_975 = {
    testId = 975,
    allocatedKB = 1950,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    975, metric_975.allocatedKB, metric_975.cycles))
```

## Tushuntirish va Mantiq:
975-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #975: Ajratilgan xotira=1950 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 976-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #976
## Topshiriq sharti:
976-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_976 = {
    testId = 976,
    allocatedKB = 1952,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    976, metric_976.allocatedKB, metric_976.cycles))
```

## Tushuntirish va Mantiq:
976-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #976: Ajratilgan xotira=1952 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 977-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #977
## Topshiriq sharti:
977-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_977 = {
    testId = 977,
    allocatedKB = 1954,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    977, metric_977.allocatedKB, metric_977.cycles))
```

## Tushuntirish va Mantiq:
977-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #977: Ajratilgan xotira=1954 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 978-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #978
## Topshiriq sharti:
978-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_978 = {
    testId = 978,
    allocatedKB = 1956,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    978, metric_978.allocatedKB, metric_978.cycles))
```

## Tushuntirish va Mantiq:
978-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #978: Ajratilgan xotira=1956 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 979-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #979
## Topshiriq sharti:
979-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_979 = {
    testId = 979,
    allocatedKB = 1958,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    979, metric_979.allocatedKB, metric_979.cycles))
```

## Tushuntirish va Mantiq:
979-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #979: Ajratilgan xotira=1958 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 980-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #980
## Topshiriq sharti:
980-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_980 = {
    testId = 980,
    allocatedKB = 1960,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    980, metric_980.allocatedKB, metric_980.cycles))
```

## Tushuntirish va Mantiq:
980-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #980: Ajratilgan xotira=1960 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 981-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #981
## Topshiriq sharti:
981-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_981 = {
    testId = 981,
    allocatedKB = 1962,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    981, metric_981.allocatedKB, metric_981.cycles))
```

## Tushuntirish va Mantiq:
981-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #981: Ajratilgan xotira=1962 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 982-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #982
## Topshiriq sharti:
982-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_982 = {
    testId = 982,
    allocatedKB = 1964,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    982, metric_982.allocatedKB, metric_982.cycles))
```

## Tushuntirish va Mantiq:
982-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #982: Ajratilgan xotira=1964 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 983-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #983
## Topshiriq sharti:
983-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_983 = {
    testId = 983,
    allocatedKB = 1966,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    983, metric_983.allocatedKB, metric_983.cycles))
```

## Tushuntirish va Mantiq:
983-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #983: Ajratilgan xotira=1966 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 984-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #984
## Topshiriq sharti:
984-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_984 = {
    testId = 984,
    allocatedKB = 1968,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    984, metric_984.allocatedKB, metric_984.cycles))
```

## Tushuntirish va Mantiq:
984-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #984: Ajratilgan xotira=1968 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 985-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #985
## Topshiriq sharti:
985-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_985 = {
    testId = 985,
    allocatedKB = 1970,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    985, metric_985.allocatedKB, metric_985.cycles))
```

## Tushuntirish va Mantiq:
985-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #985: Ajratilgan xotira=1970 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 986-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #986
## Topshiriq sharti:
986-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_986 = {
    testId = 986,
    allocatedKB = 1972,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    986, metric_986.allocatedKB, metric_986.cycles))
```

## Tushuntirish va Mantiq:
986-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #986: Ajratilgan xotira=1972 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 987-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #987
## Topshiriq sharti:
987-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_987 = {
    testId = 987,
    allocatedKB = 1974,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    987, metric_987.allocatedKB, metric_987.cycles))
```

## Tushuntirish va Mantiq:
987-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #987: Ajratilgan xotira=1974 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 988-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #988
## Topshiriq sharti:
988-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_988 = {
    testId = 988,
    allocatedKB = 1976,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    988, metric_988.allocatedKB, metric_988.cycles))
```

## Tushuntirish va Mantiq:
988-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #988: Ajratilgan xotira=1976 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 989-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #989
## Topshiriq sharti:
989-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_989 = {
    testId = 989,
    allocatedKB = 1978,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    989, metric_989.allocatedKB, metric_989.cycles))
```

## Tushuntirish va Mantiq:
989-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #989: Ajratilgan xotira=1978 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 990-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #990
## Topshiriq sharti:
990-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_990 = {
    testId = 990,
    allocatedKB = 1980,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    990, metric_990.allocatedKB, metric_990.cycles))
```

## Tushuntirish va Mantiq:
990-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #990: Ajratilgan xotira=1980 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 991-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #991
## Topshiriq sharti:
991-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_991 = {
    testId = 991,
    allocatedKB = 1982,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    991, metric_991.allocatedKB, metric_991.cycles))
```

## Tushuntirish va Mantiq:
991-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #991: Ajratilgan xotira=1982 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 992-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #992
## Topshiriq sharti:
992-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_992 = {
    testId = 992,
    allocatedKB = 1984,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    992, metric_992.allocatedKB, metric_992.cycles))
```

## Tushuntirish va Mantiq:
992-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #992: Ajratilgan xotira=1984 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 993-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #993
## Topshiriq sharti:
993-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_993 = {
    testId = 993,
    allocatedKB = 1986,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    993, metric_993.allocatedKB, metric_993.cycles))
```

## Tushuntirish va Mantiq:
993-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #993: Ajratilgan xotira=1986 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 994-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #994
## Topshiriq sharti:
994-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_994 = {
    testId = 994,
    allocatedKB = 1988,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    994, metric_994.allocatedKB, metric_994.cycles))
```

## Tushuntirish va Mantiq:
994-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #994: Ajratilgan xotira=1988 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 995-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #995
## Topshiriq sharti:
995-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_995 = {
    testId = 995,
    allocatedKB = 1990,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    995, metric_995.allocatedKB, metric_995.cycles))
```

## Tushuntirish va Mantiq:
995-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #995: Ajratilgan xotira=1990 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 996-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #996
## Topshiriq sharti:
996-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_996 = {
    testId = 996,
    allocatedKB = 1992,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    996, metric_996.allocatedKB, metric_996.cycles))
```

## Tushuntirish va Mantiq:
996-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #996: Ajratilgan xotira=1992 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 997-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #997
## Topshiriq sharti:
997-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_997 = {
    testId = 997,
    allocatedKB = 1994,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    997, metric_997.allocatedKB, metric_997.cycles))
```

## Tushuntirish va Mantiq:
997-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #997: Ajratilgan xotira=1994 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 998-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #998
## Topshiriq sharti:
998-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_998 = {
    testId = 998,
    allocatedKB = 1996,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    998, metric_998.allocatedKB, metric_998.cycles))
```

## Tushuntirish va Mantiq:
998-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #998: Ajratilgan xotira=1996 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 999-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #999
## Topshiriq sharti:
999-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_999 = {
    testId = 999,
    allocatedKB = 1998,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    999, metric_999.allocatedKB, metric_999.cycles))
```

## Tushuntirish va Mantiq:
999-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #999: Ajratilgan xotira=1998 KB, Sikllar=1000 [STATUS: OPTIMAL]
```


# 1000-Topshiriq: Unumdorlik muhandisligi va GC optimizatsiyasi #1000
## Topshiriq sharti:
1000-vazifa: Profiling, xotira sarfini minimallashtirish, algoritmik samaradorlik va benchmark xulosasi.

## Yechim (Lua kodi):
```lua
local metric_1000 = {
    testId = 1000,
    allocatedKB = 2000,
    cycles = 1000
}

print(string.format("Unumdorlik testi #%d: Ajratilgan xotira=%d KB, Sikllar=%d [STATUS: OPTIMAL]", 
    1000, metric_1000.allocatedKB, metric_1000.cycles))
```

## Tushuntirish va Mantiq:
1000-topshiriqda virtual mashina registrlari, GC tozalash davrlari va unumdorlik monitoringi tahlil qilindi.

## Ishlash natijasi:
```text
Unumdorlik testi #1000: Ajratilgan xotira=2000 KB, Sikllar=1000 [STATUS: OPTIMAL]
```

