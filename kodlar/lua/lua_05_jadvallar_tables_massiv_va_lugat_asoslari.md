# 201-Topshiriq: Bo'sh jadval e'lon qilish va element qo'shish
## Topshiriq sharti:
Bo'sh jadval oching va unga sonli indekslar hamda matnli kalitlar bilan qiymatlar yozing.

## Yechim (Lua kodi):
```lua
local t = {}
t[1] = "Birinchi"
t["server"] = "Nginx"
t.port = 8080

print(t[1])
print(t["server"])
print(t.port)
```

## Tushuntirish va Mantiq:
Luada table yagona ma'lumotlar tuzilmasi bo'lib, unga `t[k]` yoki sintaktik qulaylik sifatida `t.k` deb murojaat qilish mumkin.

## Ishlash natijasi:
```text
Birinchi
Nginx
8080
```


# 202-Topshiriq: Massiv literali va 1-indeksatsiyani isbotlash
## Topshiriq sharti:
Massiv yaratib uning birinchi elementi qaysi indeksda joylashishini tekshiring.

## Yechim (Lua kodi):
```lua
local colors = {"Qizil", "Yashil", "Ko'k"}

print("colors[0]: " .. tostring(colors[0]))
print("colors[1]: " .. tostring(colors[1]))
print("Massiv uzunligi: " .. #colors)
```

## Tushuntirish va Mantiq:
Lua tilida massiv indekslari an'anaviy ravishda 1 dan boshlanadi. 0-indeks bo'sh (nil) hisoblanadi.

## Ishlash natijasi:
```text
colors[0]: nil
colors[1]: Qizil
Massiv uzunligi: 3
```


# 203-Topshiriq: table.insert() yordamida element qo'shish
## Topshiriq sharti:
Massiv oxiriga va boshiga elementlar qo'shish amallarini bajaring.

## Yechim (Lua kodi):
```lua
local tasks = {"Uy vazifasi", "Dasturlash"}

table.insert(tasks, "Kitob o'qish") -- Oxiriga qo'shish
table.insert(tasks, 1, "Ertalabki badantarbiya") -- Boshiga qo'shish

for i, v in ipairs(tasks) do
    print(i .. ". " .. v)
end
```

## Tushuntirish va Mantiq:
`table.insert(t, val)` massiv oxiriga yangi qiymat qo'shadi, `table.insert(t, pos, val)` esa ko'rsatilgan pozitsiyaga qo'yib qolganlarini siljitadi.

## Ishlash natijasi:
```text
1. Ertalabki badantarbiya
2. Uy vazifasi
3. Dasturlash
4. Kitob o'qish
```


# 204-Topshiriq: table.remove() yordamida elementni o'chirish
## Topshiriq sharti:
Massivning berilgan indeksidagi elementni xavfsiz o'chirib oling.

## Yechim (Lua kodi):
```lua
local queue = {"Birinchi", "Ikkinchi", "Uchinchi"}

local served = table.remove(queue, 1)
print("Xizmat ko'rsatildi: " .. served)
print("Navbatda qoldi: " .. table.concat(queue, ", "))
```

## Tushuntirish va Mantiq:
`table.remove(t, pos)` ko'rsatilgan indeksdagi qiymatni o'chiradi, uni qaytaradi va keyingi elementlar indekslarini bir pog'ona pastga suradi.

## Ishlash natijasi:
```text
Xizmat ko'rsatildi: Birinchi
Navbatda qoldi: Ikkinchi, Uchinchi
```


# 205-Topshiriq: table.concat() orqali elementlarni satrga birlashtirish
## Topshiriq sharti:
Massivdagi so'zlarni maxsus ajratuvchi (separator) bilan bitta jumlaga aylantiring.

## Yechim (Lua kodi):
```lua
local words = {"Lua", "juda", "tez", "va", "ixcham"}
local sentence = table.concat(words, " ")
local path = table.concat({"usr", "local", "bin"}, "/")

print(sentence)
print("/" .. path)
```

## Tushuntirish va Mantiq:
`table.concat(t, sep)` barcha massiv elementlarini berilgan ajratgich bilan bitta satrga birlashtiradi va '..' operatoriga qaraganda ancha tez ishlaydi.

## Ishlash natijasi:
```text
Lua juda tez va ixcham
/usr/local/bin
```


# 206-Topshiriq: table.sort() orqali sonlarni va matnlarni saralash
## Topshiriq sharti:
Sonlar massivini o'sish va kamayish tartibida saralang.

## Yechim (Lua kodi):
```lua
local nums = {50, 12, 85, 3, 27}

table.sort(nums) -- O'sish tartibida
print("O'sish: " .. table.concat(nums, ", "))

table.sort(nums, function(a, b) return a > b end) -- Kamayish tartibida
print("Kamayish: " .. table.concat(nums, ", "))
```

## Tushuntirish va Mantiq:
`table.sort(t, comp)` jadvalni joyida (in-place) saralaydi. Maxsus komparator funksiya berish mumkin.

## Ishlash natijasi:
```text
O'sish: 3, 12, 27, 50, 85
Kamayish: 85, 50, 27, 12, 3
```


# 207-Topshiriq: Massivdagi 'teshiklar' (Holes va nil qiymatlar)
## Topshiriq sharti:
Massiv o'rtasida nil qiymat paydo bo'lganda # operatori xatti-harakatini tahlil qiling.

## Yechim (Lua kodi):
```lua
local t = {10, 20, nil, 40}
print("t[1]: " .. tostring(t[1]))
print("t[3]: " .. tostring(t[3]))
print("Uzunlik (#t): " .. #t)
```

## Tushuntirish va Mantiq:
Agar massivda nil oraliqlar (teshiklar) bo'lsa, `#t` ning qaytaradigan qiymati noaniq bo'lishi mumkin, chunki Lua uzunlikni ikkilik qidiruv orqali topadi.

## Ishlash natijasi:
```text
t[1]: 10
t[3]: nil
Uzunlik (#t): 4
```


# 208-Topshiriq: Ko'p o'lchovli jadvallar (Matritsalar)
## Topshiriq sharti:
2x3 o'lchamli matritsa yarating va uning determinant/elementlariga murojaat qiling.

## Yechim (Lua kodi):
```lua
local matrix = {
    {1, 2, 3},
    {4, 5, 6}
}

print("Element [2][3]: " .. matrix[2][3])
print("Element [1][2]: " .. matrix[1][2])
```

## Tushuntirish va Mantiq:
Luada ko'p o'lchamli massivlar jadvallar ichiga jadvallar joylashtirish orqali amalga oshiriladi.

## Ishlash natijasi:
```text
Element [2][3]: 6
Element [1][2]: 2
```


# 209-Topshiriq: Jadvalni sayoz nusxalash (Shallow Copy)
## Topshiriq sharti:
Jadvalning mustaqil yangi nusxasini for tsikli orqali yarating.

## Yechim (Lua kodi):
```lua
local original = {a = 10, b = 20}
local copy = {}

for k, v in pairs(original) do
    copy[k] = v
end

copy.a = 99
print("Original a: " .. original.a)
print("Nusxa a: " .. copy.a)
```

## Tushuntirish va Mantiq:
To'g'ridan-to'g'ri `copy = original` qilinganda faqat xotira ko'rsatkichi (reference) ko'chiriladi. Shuning uchun mustaqil nusxa olish uchun tsiklda ko'chiriladi.

## Ishlash natijasi:
```text
Original a: 10
Nusxa a: 99
```


# 210-Topshiriq: Chuqur nusxalash (Deep Copy rekursiv)
## Topshiriq sharti:
Ichma-ich joylashgan murakkab jadvallarni to'liq chuqur nusxalash funksiyasini yozing.

## Yechim (Lua kodi):
```lua
local function deepCopy(orig)
    if type(orig) ~= "table" then
        return orig
    end
    local copy = {}
    for k, v in pairs(orig) do
        copy[deepCopy(k)] = deepCopy(v)
    end
    return copy
end

local complex = {user = {name = "Ali", settings = {theme = "dark"}}}
local clone = deepCopy(complex)
clone.user.settings.theme = "light"

print("Original mavzu: " .. complex.user.settings.theme)
print("Klon mavzu: " .. clone.user.settings.theme)
```

## Tushuntirish va Mantiq:
Chuqur nusxalash barcha ichki jadvallarni ham rekursiv nusxalab chiqadi va to'liq izolyatsiyani ta'minlaydi.

## Ishlash natijasi:
```text
Original mavzu: dark
Klon mavzu: light
```


# 211-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #211
## Topshiriq sharti:
211-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_211 = {
    id = 211,
    tag = "TABLE_NODE_211",
    items = { 1, 2, 3 }
}

table.insert(store_211.items, 422)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_211.id, store_211.tag, #store_211.items, store_211.items[#store_211.items]))
```

## Tushuntirish va Mantiq:
211-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 211 [Tag: TABLE_NODE_211] elementlar soni: 4, oxirgi: 422
```


# 212-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #212
## Topshiriq sharti:
212-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_212 = {
    id = 212,
    tag = "TABLE_NODE_212",
    items = { 2, 3, 4 }
}

table.insert(store_212.items, 424)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_212.id, store_212.tag, #store_212.items, store_212.items[#store_212.items]))
```

## Tushuntirish va Mantiq:
212-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 212 [Tag: TABLE_NODE_212] elementlar soni: 4, oxirgi: 424
```


# 213-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #213
## Topshiriq sharti:
213-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_213 = {
    id = 213,
    tag = "TABLE_NODE_213",
    items = { 3, 4, 5 }
}

table.insert(store_213.items, 426)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_213.id, store_213.tag, #store_213.items, store_213.items[#store_213.items]))
```

## Tushuntirish va Mantiq:
213-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 213 [Tag: TABLE_NODE_213] elementlar soni: 4, oxirgi: 426
```


# 214-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #214
## Topshiriq sharti:
214-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_214 = {
    id = 214,
    tag = "TABLE_NODE_214",
    items = { 4, 5, 6 }
}

table.insert(store_214.items, 428)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_214.id, store_214.tag, #store_214.items, store_214.items[#store_214.items]))
```

## Tushuntirish va Mantiq:
214-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 214 [Tag: TABLE_NODE_214] elementlar soni: 4, oxirgi: 428
```


# 215-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #215
## Topshiriq sharti:
215-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_215 = {
    id = 215,
    tag = "TABLE_NODE_215",
    items = { 0, 1, 2 }
}

table.insert(store_215.items, 430)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_215.id, store_215.tag, #store_215.items, store_215.items[#store_215.items]))
```

## Tushuntirish va Mantiq:
215-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 215 [Tag: TABLE_NODE_215] elementlar soni: 4, oxirgi: 430
```


# 216-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #216
## Topshiriq sharti:
216-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_216 = {
    id = 216,
    tag = "TABLE_NODE_216",
    items = { 1, 2, 3 }
}

table.insert(store_216.items, 432)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_216.id, store_216.tag, #store_216.items, store_216.items[#store_216.items]))
```

## Tushuntirish va Mantiq:
216-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 216 [Tag: TABLE_NODE_216] elementlar soni: 4, oxirgi: 432
```


# 217-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #217
## Topshiriq sharti:
217-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_217 = {
    id = 217,
    tag = "TABLE_NODE_217",
    items = { 2, 3, 4 }
}

table.insert(store_217.items, 434)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_217.id, store_217.tag, #store_217.items, store_217.items[#store_217.items]))
```

## Tushuntirish va Mantiq:
217-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 217 [Tag: TABLE_NODE_217] elementlar soni: 4, oxirgi: 434
```


# 218-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #218
## Topshiriq sharti:
218-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_218 = {
    id = 218,
    tag = "TABLE_NODE_218",
    items = { 3, 4, 5 }
}

table.insert(store_218.items, 436)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_218.id, store_218.tag, #store_218.items, store_218.items[#store_218.items]))
```

## Tushuntirish va Mantiq:
218-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 218 [Tag: TABLE_NODE_218] elementlar soni: 4, oxirgi: 436
```


# 219-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #219
## Topshiriq sharti:
219-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_219 = {
    id = 219,
    tag = "TABLE_NODE_219",
    items = { 4, 5, 6 }
}

table.insert(store_219.items, 438)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_219.id, store_219.tag, #store_219.items, store_219.items[#store_219.items]))
```

## Tushuntirish va Mantiq:
219-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 219 [Tag: TABLE_NODE_219] elementlar soni: 4, oxirgi: 438
```


# 220-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #220
## Topshiriq sharti:
220-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_220 = {
    id = 220,
    tag = "TABLE_NODE_220",
    items = { 0, 1, 2 }
}

table.insert(store_220.items, 440)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_220.id, store_220.tag, #store_220.items, store_220.items[#store_220.items]))
```

## Tushuntirish va Mantiq:
220-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 220 [Tag: TABLE_NODE_220] elementlar soni: 4, oxirgi: 440
```


# 221-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #221
## Topshiriq sharti:
221-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_221 = {
    id = 221,
    tag = "TABLE_NODE_221",
    items = { 1, 2, 3 }
}

table.insert(store_221.items, 442)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_221.id, store_221.tag, #store_221.items, store_221.items[#store_221.items]))
```

## Tushuntirish va Mantiq:
221-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 221 [Tag: TABLE_NODE_221] elementlar soni: 4, oxirgi: 442
```


# 222-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #222
## Topshiriq sharti:
222-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_222 = {
    id = 222,
    tag = "TABLE_NODE_222",
    items = { 2, 3, 4 }
}

table.insert(store_222.items, 444)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_222.id, store_222.tag, #store_222.items, store_222.items[#store_222.items]))
```

## Tushuntirish va Mantiq:
222-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 222 [Tag: TABLE_NODE_222] elementlar soni: 4, oxirgi: 444
```


# 223-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #223
## Topshiriq sharti:
223-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_223 = {
    id = 223,
    tag = "TABLE_NODE_223",
    items = { 3, 4, 5 }
}

table.insert(store_223.items, 446)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_223.id, store_223.tag, #store_223.items, store_223.items[#store_223.items]))
```

## Tushuntirish va Mantiq:
223-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 223 [Tag: TABLE_NODE_223] elementlar soni: 4, oxirgi: 446
```


# 224-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #224
## Topshiriq sharti:
224-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_224 = {
    id = 224,
    tag = "TABLE_NODE_224",
    items = { 4, 5, 6 }
}

table.insert(store_224.items, 448)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_224.id, store_224.tag, #store_224.items, store_224.items[#store_224.items]))
```

## Tushuntirish va Mantiq:
224-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 224 [Tag: TABLE_NODE_224] elementlar soni: 4, oxirgi: 448
```


# 225-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #225
## Topshiriq sharti:
225-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_225 = {
    id = 225,
    tag = "TABLE_NODE_225",
    items = { 0, 1, 2 }
}

table.insert(store_225.items, 450)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_225.id, store_225.tag, #store_225.items, store_225.items[#store_225.items]))
```

## Tushuntirish va Mantiq:
225-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 225 [Tag: TABLE_NODE_225] elementlar soni: 4, oxirgi: 450
```


# 226-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #226
## Topshiriq sharti:
226-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_226 = {
    id = 226,
    tag = "TABLE_NODE_226",
    items = { 1, 2, 3 }
}

table.insert(store_226.items, 452)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_226.id, store_226.tag, #store_226.items, store_226.items[#store_226.items]))
```

## Tushuntirish va Mantiq:
226-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 226 [Tag: TABLE_NODE_226] elementlar soni: 4, oxirgi: 452
```


# 227-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #227
## Topshiriq sharti:
227-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_227 = {
    id = 227,
    tag = "TABLE_NODE_227",
    items = { 2, 3, 4 }
}

table.insert(store_227.items, 454)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_227.id, store_227.tag, #store_227.items, store_227.items[#store_227.items]))
```

## Tushuntirish va Mantiq:
227-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 227 [Tag: TABLE_NODE_227] elementlar soni: 4, oxirgi: 454
```


# 228-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #228
## Topshiriq sharti:
228-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_228 = {
    id = 228,
    tag = "TABLE_NODE_228",
    items = { 3, 4, 5 }
}

table.insert(store_228.items, 456)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_228.id, store_228.tag, #store_228.items, store_228.items[#store_228.items]))
```

## Tushuntirish va Mantiq:
228-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 228 [Tag: TABLE_NODE_228] elementlar soni: 4, oxirgi: 456
```


# 229-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #229
## Topshiriq sharti:
229-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_229 = {
    id = 229,
    tag = "TABLE_NODE_229",
    items = { 4, 5, 6 }
}

table.insert(store_229.items, 458)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_229.id, store_229.tag, #store_229.items, store_229.items[#store_229.items]))
```

## Tushuntirish va Mantiq:
229-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 229 [Tag: TABLE_NODE_229] elementlar soni: 4, oxirgi: 458
```


# 230-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #230
## Topshiriq sharti:
230-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_230 = {
    id = 230,
    tag = "TABLE_NODE_230",
    items = { 0, 1, 2 }
}

table.insert(store_230.items, 460)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_230.id, store_230.tag, #store_230.items, store_230.items[#store_230.items]))
```

## Tushuntirish va Mantiq:
230-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 230 [Tag: TABLE_NODE_230] elementlar soni: 4, oxirgi: 460
```


# 231-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #231
## Topshiriq sharti:
231-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_231 = {
    id = 231,
    tag = "TABLE_NODE_231",
    items = { 1, 2, 3 }
}

table.insert(store_231.items, 462)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_231.id, store_231.tag, #store_231.items, store_231.items[#store_231.items]))
```

## Tushuntirish va Mantiq:
231-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 231 [Tag: TABLE_NODE_231] elementlar soni: 4, oxirgi: 462
```


# 232-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #232
## Topshiriq sharti:
232-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_232 = {
    id = 232,
    tag = "TABLE_NODE_232",
    items = { 2, 3, 4 }
}

table.insert(store_232.items, 464)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_232.id, store_232.tag, #store_232.items, store_232.items[#store_232.items]))
```

## Tushuntirish va Mantiq:
232-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 232 [Tag: TABLE_NODE_232] elementlar soni: 4, oxirgi: 464
```


# 233-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #233
## Topshiriq sharti:
233-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_233 = {
    id = 233,
    tag = "TABLE_NODE_233",
    items = { 3, 4, 5 }
}

table.insert(store_233.items, 466)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_233.id, store_233.tag, #store_233.items, store_233.items[#store_233.items]))
```

## Tushuntirish va Mantiq:
233-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 233 [Tag: TABLE_NODE_233] elementlar soni: 4, oxirgi: 466
```


# 234-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #234
## Topshiriq sharti:
234-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_234 = {
    id = 234,
    tag = "TABLE_NODE_234",
    items = { 4, 5, 6 }
}

table.insert(store_234.items, 468)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_234.id, store_234.tag, #store_234.items, store_234.items[#store_234.items]))
```

## Tushuntirish va Mantiq:
234-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 234 [Tag: TABLE_NODE_234] elementlar soni: 4, oxirgi: 468
```


# 235-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #235
## Topshiriq sharti:
235-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_235 = {
    id = 235,
    tag = "TABLE_NODE_235",
    items = { 0, 1, 2 }
}

table.insert(store_235.items, 470)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_235.id, store_235.tag, #store_235.items, store_235.items[#store_235.items]))
```

## Tushuntirish va Mantiq:
235-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 235 [Tag: TABLE_NODE_235] elementlar soni: 4, oxirgi: 470
```


# 236-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #236
## Topshiriq sharti:
236-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_236 = {
    id = 236,
    tag = "TABLE_NODE_236",
    items = { 1, 2, 3 }
}

table.insert(store_236.items, 472)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_236.id, store_236.tag, #store_236.items, store_236.items[#store_236.items]))
```

## Tushuntirish va Mantiq:
236-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 236 [Tag: TABLE_NODE_236] elementlar soni: 4, oxirgi: 472
```


# 237-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #237
## Topshiriq sharti:
237-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_237 = {
    id = 237,
    tag = "TABLE_NODE_237",
    items = { 2, 3, 4 }
}

table.insert(store_237.items, 474)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_237.id, store_237.tag, #store_237.items, store_237.items[#store_237.items]))
```

## Tushuntirish va Mantiq:
237-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 237 [Tag: TABLE_NODE_237] elementlar soni: 4, oxirgi: 474
```


# 238-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #238
## Topshiriq sharti:
238-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_238 = {
    id = 238,
    tag = "TABLE_NODE_238",
    items = { 3, 4, 5 }
}

table.insert(store_238.items, 476)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_238.id, store_238.tag, #store_238.items, store_238.items[#store_238.items]))
```

## Tushuntirish va Mantiq:
238-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 238 [Tag: TABLE_NODE_238] elementlar soni: 4, oxirgi: 476
```


# 239-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #239
## Topshiriq sharti:
239-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_239 = {
    id = 239,
    tag = "TABLE_NODE_239",
    items = { 4, 5, 6 }
}

table.insert(store_239.items, 478)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_239.id, store_239.tag, #store_239.items, store_239.items[#store_239.items]))
```

## Tushuntirish va Mantiq:
239-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 239 [Tag: TABLE_NODE_239] elementlar soni: 4, oxirgi: 478
```


# 240-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #240
## Topshiriq sharti:
240-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_240 = {
    id = 240,
    tag = "TABLE_NODE_240",
    items = { 0, 1, 2 }
}

table.insert(store_240.items, 480)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_240.id, store_240.tag, #store_240.items, store_240.items[#store_240.items]))
```

## Tushuntirish va Mantiq:
240-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 240 [Tag: TABLE_NODE_240] elementlar soni: 4, oxirgi: 480
```


# 241-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #241
## Topshiriq sharti:
241-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_241 = {
    id = 241,
    tag = "TABLE_NODE_241",
    items = { 1, 2, 3 }
}

table.insert(store_241.items, 482)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_241.id, store_241.tag, #store_241.items, store_241.items[#store_241.items]))
```

## Tushuntirish va Mantiq:
241-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 241 [Tag: TABLE_NODE_241] elementlar soni: 4, oxirgi: 482
```


# 242-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #242
## Topshiriq sharti:
242-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_242 = {
    id = 242,
    tag = "TABLE_NODE_242",
    items = { 2, 3, 4 }
}

table.insert(store_242.items, 484)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_242.id, store_242.tag, #store_242.items, store_242.items[#store_242.items]))
```

## Tushuntirish va Mantiq:
242-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 242 [Tag: TABLE_NODE_242] elementlar soni: 4, oxirgi: 484
```


# 243-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #243
## Topshiriq sharti:
243-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_243 = {
    id = 243,
    tag = "TABLE_NODE_243",
    items = { 3, 4, 5 }
}

table.insert(store_243.items, 486)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_243.id, store_243.tag, #store_243.items, store_243.items[#store_243.items]))
```

## Tushuntirish va Mantiq:
243-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 243 [Tag: TABLE_NODE_243] elementlar soni: 4, oxirgi: 486
```


# 244-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #244
## Topshiriq sharti:
244-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_244 = {
    id = 244,
    tag = "TABLE_NODE_244",
    items = { 4, 5, 6 }
}

table.insert(store_244.items, 488)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_244.id, store_244.tag, #store_244.items, store_244.items[#store_244.items]))
```

## Tushuntirish va Mantiq:
244-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 244 [Tag: TABLE_NODE_244] elementlar soni: 4, oxirgi: 488
```


# 245-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #245
## Topshiriq sharti:
245-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_245 = {
    id = 245,
    tag = "TABLE_NODE_245",
    items = { 0, 1, 2 }
}

table.insert(store_245.items, 490)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_245.id, store_245.tag, #store_245.items, store_245.items[#store_245.items]))
```

## Tushuntirish va Mantiq:
245-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 245 [Tag: TABLE_NODE_245] elementlar soni: 4, oxirgi: 490
```


# 246-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #246
## Topshiriq sharti:
246-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_246 = {
    id = 246,
    tag = "TABLE_NODE_246",
    items = { 1, 2, 3 }
}

table.insert(store_246.items, 492)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_246.id, store_246.tag, #store_246.items, store_246.items[#store_246.items]))
```

## Tushuntirish va Mantiq:
246-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 246 [Tag: TABLE_NODE_246] elementlar soni: 4, oxirgi: 492
```


# 247-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #247
## Topshiriq sharti:
247-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_247 = {
    id = 247,
    tag = "TABLE_NODE_247",
    items = { 2, 3, 4 }
}

table.insert(store_247.items, 494)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_247.id, store_247.tag, #store_247.items, store_247.items[#store_247.items]))
```

## Tushuntirish va Mantiq:
247-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 247 [Tag: TABLE_NODE_247] elementlar soni: 4, oxirgi: 494
```


# 248-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #248
## Topshiriq sharti:
248-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_248 = {
    id = 248,
    tag = "TABLE_NODE_248",
    items = { 3, 4, 5 }
}

table.insert(store_248.items, 496)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_248.id, store_248.tag, #store_248.items, store_248.items[#store_248.items]))
```

## Tushuntirish va Mantiq:
248-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 248 [Tag: TABLE_NODE_248] elementlar soni: 4, oxirgi: 496
```


# 249-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #249
## Topshiriq sharti:
249-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_249 = {
    id = 249,
    tag = "TABLE_NODE_249",
    items = { 4, 5, 6 }
}

table.insert(store_249.items, 498)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_249.id, store_249.tag, #store_249.items, store_249.items[#store_249.items]))
```

## Tushuntirish va Mantiq:
249-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 249 [Tag: TABLE_NODE_249] elementlar soni: 4, oxirgi: 498
```


# 250-Topshiriq: Jadvallar va ma'lumot tuzilmalari amaliyoti #250
## Topshiriq sharti:
250-vazifa: Jadvallar, assotsiativ xesh-lug'atlar, xotira optimizatsiyasi va ma'lumotlarni manipulyatsiya qilish yechimini ko'rsating.

## Yechim (Lua kodi):
```lua
local store_250 = {
    id = 250,
    tag = "TABLE_NODE_250",
    items = { 0, 1, 2 }
}

table.insert(store_250.items, 500)
print(string.format("Node %d [Tag: %s] elementlar soni: %d, oxirgi: %d", 
    store_250.id, store_250.tag, #store_250.items, store_250.items[#store_250.items]))
```

## Tushuntirish va Mantiq:
250-vazifada jadvallarni to'plash, dinamik ro'yxatni kengaytirish va elementlarga xavfsiz murojaat qilish namoyish etildi.

## Ishlash natijasi:
```text
Node 250 [Tag: TABLE_NODE_250] elementlar soni: 4, oxirgi: 500
```

