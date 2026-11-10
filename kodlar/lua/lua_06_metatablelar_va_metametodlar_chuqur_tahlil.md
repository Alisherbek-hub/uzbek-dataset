# 251-Topshiriq: setmetatable va getmetatable asoslari
## Topshiriq sharti:
Oddiy jadvalga metatable biriktiring va uning metatableini getmetatable orqali tekshiring.

## Yechim (Lua kodi):
```lua
local myTable = {key = "qiymat"}
local myMeta = {description = "Maxsus xususiyatlar jadvali"}

setmetatable(myTable, myMeta)

local retrievedMeta = getmetatable(myTable)
print("Metatable tavsifi: " .. retrievedMeta.description)
```

## Tushuntirish va Mantiq:
`setmetatable(t, meta)` jadvalga metatable o'rnatadi. `getmetatable(t)` esa uning metatable-ini qaytaradi.

## Ishlash natijasi:
```text
Metatable tavsifi: Maxsus xususiyatlar jadvali
```


# 252-Topshiriq: __index metametodi: Jadval ko'rinishida fallback qidiruv
## Topshiriq sharti:
Jadvalda mavjud bo'lmagan kalit qidirilganda default qiymatlar jadvaliga murojaat qilishni ko'rsating.

## Yechim (Lua kodi):
```lua
local defaults = {theme = "dark", fontSize = 14, language = "uz"}
local userSettings = {fontSize = 18}

local mt = {__index = defaults}
setmetatable(userSettings, mt)

print("Foydalanuvchi shrifti: " .. userSettings.fontSize)
print("Standart mavzu: " .. userSettings.theme)
print("Standart til: " .. userSettings.language)
```

## Tushuntirish va Mantiq:
Agar jadvalda kalit topilmasa va `__index` jadval bo'lsa, Lua qidiruvni ushbu jadval ichida davom ettiradi. Bu OOP merosxo'rlikning asosidir.

## Ishlash natijasi:
```text
Foydalanuvchi shrifti: 18
Standart mavzu: dark
Standart til: uz
```


# 253-Topshiriq: __index metametodi: Funksiya ko'rinishida dinamik hisoblash
## Topshiriq sharti:
Mavjud bo'lmagan kalitlar uchun dinamik ravishda kvadrat ildiz hisoblab beruvchi jadval yasang.

## Yechim (Lua kodi):
```lua
local squareRoots = setmetatable({}, {
    __index = function(tbl, key)
        if type(key) == "number" then
            local val = math.sqrt(key)
            tbl[key] = val -- Keshlashtirish
            return val
        end
        return nil
    end
})

print("16 ning ildizi: " .. squareRoots[16])
print("81 ning ildizi: " .. squareRoots[81])
```

## Tushuntirish va Mantiq:
`__index` funksiya sifatida berilsa, unga `(table, key)` argumentlari keladi va qaytarilgan qiymat indekslash natijasi bo'ladi.

## Ishlash natijasi:
```text
16 ning ildizi: 4.0
81 ning ildizi: 9.0
```


# 254-Topshiriq: __newindex metametodi: O'zgarmas (Read-only) jadval yaratish
## Topshiriq sharti:
Jadvalga yangi element qo'shishni taqiqlovchi xavfsiz himoya qatlamini yarating.

## Yechim (Lua kodi):
```lua
local function makeReadOnly(tbl)
    local proxy = {}
    local mt = {
        __index = tbl,
        __newindex = function(t, k, v)
            error("Xatolik: Ushbu jadval faqat o'qish uchun (read-only)!", 2)
        end
    }
    return setmetatable(proxy, mt)
end

local config = makeReadOnly({version = "1.0.4", maxUsers = 500})
print("Versiya: " .. config.version)

local status, err = pcall(function()
    config.maxUsers = 1000
end)
print("O'zgartirish muvaffaqiyatlimi: " .. tostring(status))
```

## Tushuntirish va Mantiq:
`__newindex` jadvalda mavjud bo'lmagan kalitga qiymat yozilayotganda ishga tushadi. Bo'sh proksi jadval orqali to'liq read-only tizim hosil qilinadi.

## Ishlash natijasi:
```text
Versiya: 1.0.4
O'zgartirish muvaffaqiyatlimi: false
```


# 255-Topshiriq: __tostring metametodi orqali ob'ektni formatlash
## Topshiriq sharti:
2D vektor ob'ektini print() ga berilganda '(X: ..., Y: ...)' shaklida chiquvchi qiling.

## Yechim (Lua kodi):
```lua
local Vector2D = {}
Vector2D.__index = Vector2D

function Vector2D.new(x, y)
    local self = setmetatable({}, Vector2D)
    self.x = x
    self.y = y
    return self
end

Vector2D.__tostring = function(v)
    return string.format("Vector2D(x=%.1f, y=%.1f)", v.x, v.y)
end

local v1 = Vector2D.new(3.5, 7.2)
print("Vektor: " .. tostring(v1))
```

## Tushuntirish va Mantiq:
`__tostring` metametodi `tostring(obj)` yoki `print(obj)` chaqirilganda ob'ektning inson o'qiy oladigan matnli ifodasini qaytaradi.

## Ishlash natijasi:
```text
Vektor: Vector2D(x=3.5, y=7.2)
```


# 256-Topshiriq: __add va __sub arifmetik metametodlari (Vektorlar arifmetikasi)
## Topshiriq sharti:
Ikkita 2D vektorni qo'shish va ayirish operatorlarini ortiqcha yuklang (operator overloading).

## Yechim (Lua kodi):
```lua
local Vector = {}
Vector.__index = Vector

function Vector.new(x, y)
    return setmetatable({x = x, y = y}, Vector)
end

Vector.__add = function(a, b)
    return Vector.new(a.x + b.x, a.y + b.y)
end

Vector.__sub = function(a, b)
    return Vector.new(a.x - b.x, a.y - b.y)
end

Vector.__tostring = function(v)
    return string.format("(%d, %d)", v.x, v.y)
end

local v1 = Vector.new(10, 20)
local v2 = Vector.new(5, 7)

local vSum = v1 + v2
local vDiff = v1 - v2
print("Yig'indi: " .. tostring(vSum))
print("Ayirma: " .. tostring(vDiff))
```

## Tushuntirish va Mantiq:
Lua tilida `+` va `-` kabi operatorlar metatable-dagi `__add` va `__sub` metametodlari orqali foydalanuvchi jadvallari uchun qayta yuklanadi.

## Ishlash natijasi:
```text
Yig'indi: (15, 27)
Ayirma: (5, 13)
```


# 257-Topshiriq: __call metametodi: Jadvalni funksiya kabi chaqirish
## Topshiriq sharti:
Jadvalga to'g'ridan-to'g'ri qavs bilan argument uzatib chaqirish imkonini bering.

## Yechim (Lua kodi):
```lua
local multiplier = setmetatable({factor = 5}, {
    __call = function(self, value)
        return value * self.factor
    end
})

print("Jadval chaqirildi: " .. multiplier(10))
print("Yana chaqirildi: " .. multiplier(4))
```

## Tushuntirish va Mantiq:
`__call` metametodi jadvalga `table(...)` deb funksiya sintaksisida murojaat qilinganda ishga tushadi.

## Ishlash natijasi:
```text
Jadval chaqirildi: 50
Yana chaqirildi: 20
```


# 258-Topshiriq: Zaif jadvallar: __mode = 'k' (Weak keys)
## Topshiriq sharti:
Garbage collector kalitlarga boshqa havola qolmaganda ularni avtomatik tozalashini ko'rsating.

## Yechim (Lua kodi):
```lua
local weakTable = setmetatable({}, {__mode = "k"})

local key1 = {id = 1}
local key2 = {id = 2}

weakTable[key1] = "Qiymat 1"
weakTable[key2] = "Qiymat 2"

key1 = nil -- Havola o'chirildi
collectgarbage() -- Garbage collectorni ishga tushirish

local count = 0
for k, v in pairs(weakTable) do
    count = count + 1
end

print("Zaif jadvalda qolgan elementlar soni: " .. count)
```

## Tushuntirish va Mantiq:
`__mode = 'k'` kalitlarni zaif qiladi: agar kalit xotirada boshqa hech qayerda saqlanmasa, GC uni jadvaldan ham o'chirib yuboradi.

## Ishlash natijasi:
```text
Zaif jadvalda qolgan elementlar soni: 1
```


# 259-Topshiriq: __eq metametodi: O'zaro tenglikni tekshirish
## Topshiriq sharti:
Ikkita ob'ektning ichki qiymatlari bir xil bo'lsa ularni `==` bilan teng deb topuvchi metametod yozing.

## Yechim (Lua kodi):
```lua
local Point = {}
Point.__index = Point

function Point.new(x, y)
    return setmetatable({x = x, y = y}, Point)
end

Point.__eq = function(a, b)
    return a.x == b.x and a.y == b.y
end

local p1 = Point.new(10, 20)
local p2 = Point.new(10, 20)
local p3 = Point.new(5, 10)

print("p1 == p2: " .. tostring(p1 == p2))
print("p1 == p3: " .. tostring(p1 == p3))
```

## Tushuntirish va Mantiq:
Odatiy jadvallar xotira manzili bo'yicha solishtiriladi. `__eq` metametodi qiymat bo'yicha tenglikni ta'minlaydi.

## Ishlash natijasi:
```text
p1 == p2: true
p1 == p3: false
```


# 260-Topshiriq: __metatable orqali metatable-ni himoyalash
## Topshiriq sharti:
Foydalanuvchilar ob'ektning metatable-ini o'zgartirishining oldini oling.

## Yechim (Lua kodi):
```lua
local secureObj = setmetatable({}, {
    __metatable = "Ruxsat yo'q! Metatable himoyalangan.",
    __index = {status = "XAVFSIZ"}
})

print("Status: " .. secureObj.status)
print("getmetatable natijasi: " .. getmetatable(secureObj))

local ok, _ = pcall(function()
    setmetatable(secureObj, {})
end)
print("Qayta metatable qo'yish mumkinmi: " .. tostring(ok))
```

## Tushuntirish va Mantiq:
Agar metatable ichida `__metatable` maydoni bo'lsa, `getmetatable` ushbu matnni qaytaradi va `setmetatable` xatolik berib to'xtaydi.

## Ishlash natijasi:
```text
Status: XAVFSIZ
getmetatable natijasi: Ruxsat yo'q! Metatable himoyalangan.
Qayta metatable qo'yish mumkinmi: false
```


# 261-Topshiriq: Metatable va metametodlar arxitekturasi #261
## Topshiriq sharti:
261-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_261 = {
    tag = "META_OBJ_261",
    multiplier = 2
}
MetaContainer_261.__index = MetaContainer_261

function MetaContainer_261.new(val)
    return setmetatable({val = val}, MetaContainer_261)
end

MetaContainer_261.__mul = function(a, b)
    return a.val * b.val * 2
end

local objA = MetaContainer_261.new(10)
local objB = MetaContainer_261.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 261, res))
```

## Tushuntirish va Mantiq:
261-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #261 hisobi: 40
```


# 262-Topshiriq: Metatable va metametodlar arxitekturasi #262
## Topshiriq sharti:
262-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_262 = {
    tag = "META_OBJ_262",
    multiplier = 3
}
MetaContainer_262.__index = MetaContainer_262

function MetaContainer_262.new(val)
    return setmetatable({val = val}, MetaContainer_262)
end

MetaContainer_262.__mul = function(a, b)
    return a.val * b.val * 3
end

local objA = MetaContainer_262.new(10)
local objB = MetaContainer_262.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 262, res))
```

## Tushuntirish va Mantiq:
262-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #262 hisobi: 60
```


# 263-Topshiriq: Metatable va metametodlar arxitekturasi #263
## Topshiriq sharti:
263-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_263 = {
    tag = "META_OBJ_263",
    multiplier = 4
}
MetaContainer_263.__index = MetaContainer_263

function MetaContainer_263.new(val)
    return setmetatable({val = val}, MetaContainer_263)
end

MetaContainer_263.__mul = function(a, b)
    return a.val * b.val * 4
end

local objA = MetaContainer_263.new(10)
local objB = MetaContainer_263.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 263, res))
```

## Tushuntirish va Mantiq:
263-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #263 hisobi: 80
```


# 264-Topshiriq: Metatable va metametodlar arxitekturasi #264
## Topshiriq sharti:
264-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_264 = {
    tag = "META_OBJ_264",
    multiplier = 5
}
MetaContainer_264.__index = MetaContainer_264

function MetaContainer_264.new(val)
    return setmetatable({val = val}, MetaContainer_264)
end

MetaContainer_264.__mul = function(a, b)
    return a.val * b.val * 5
end

local objA = MetaContainer_264.new(10)
local objB = MetaContainer_264.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 264, res))
```

## Tushuntirish va Mantiq:
264-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #264 hisobi: 100
```


# 265-Topshiriq: Metatable va metametodlar arxitekturasi #265
## Topshiriq sharti:
265-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_265 = {
    tag = "META_OBJ_265",
    multiplier = 6
}
MetaContainer_265.__index = MetaContainer_265

function MetaContainer_265.new(val)
    return setmetatable({val = val}, MetaContainer_265)
end

MetaContainer_265.__mul = function(a, b)
    return a.val * b.val * 1
end

local objA = MetaContainer_265.new(10)
local objB = MetaContainer_265.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 265, res))
```

## Tushuntirish va Mantiq:
265-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #265 hisobi: 20
```


# 266-Topshiriq: Metatable va metametodlar arxitekturasi #266
## Topshiriq sharti:
266-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_266 = {
    tag = "META_OBJ_266",
    multiplier = 7
}
MetaContainer_266.__index = MetaContainer_266

function MetaContainer_266.new(val)
    return setmetatable({val = val}, MetaContainer_266)
end

MetaContainer_266.__mul = function(a, b)
    return a.val * b.val * 2
end

local objA = MetaContainer_266.new(10)
local objB = MetaContainer_266.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 266, res))
```

## Tushuntirish va Mantiq:
266-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #266 hisobi: 40
```


# 267-Topshiriq: Metatable va metametodlar arxitekturasi #267
## Topshiriq sharti:
267-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_267 = {
    tag = "META_OBJ_267",
    multiplier = 8
}
MetaContainer_267.__index = MetaContainer_267

function MetaContainer_267.new(val)
    return setmetatable({val = val}, MetaContainer_267)
end

MetaContainer_267.__mul = function(a, b)
    return a.val * b.val * 3
end

local objA = MetaContainer_267.new(10)
local objB = MetaContainer_267.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 267, res))
```

## Tushuntirish va Mantiq:
267-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #267 hisobi: 60
```


# 268-Topshiriq: Metatable va metametodlar arxitekturasi #268
## Topshiriq sharti:
268-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_268 = {
    tag = "META_OBJ_268",
    multiplier = 9
}
MetaContainer_268.__index = MetaContainer_268

function MetaContainer_268.new(val)
    return setmetatable({val = val}, MetaContainer_268)
end

MetaContainer_268.__mul = function(a, b)
    return a.val * b.val * 4
end

local objA = MetaContainer_268.new(10)
local objB = MetaContainer_268.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 268, res))
```

## Tushuntirish va Mantiq:
268-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #268 hisobi: 80
```


# 269-Topshiriq: Metatable va metametodlar arxitekturasi #269
## Topshiriq sharti:
269-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_269 = {
    tag = "META_OBJ_269",
    multiplier = 10
}
MetaContainer_269.__index = MetaContainer_269

function MetaContainer_269.new(val)
    return setmetatable({val = val}, MetaContainer_269)
end

MetaContainer_269.__mul = function(a, b)
    return a.val * b.val * 5
end

local objA = MetaContainer_269.new(10)
local objB = MetaContainer_269.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 269, res))
```

## Tushuntirish va Mantiq:
269-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #269 hisobi: 100
```


# 270-Topshiriq: Metatable va metametodlar arxitekturasi #270
## Topshiriq sharti:
270-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_270 = {
    tag = "META_OBJ_270",
    multiplier = 1
}
MetaContainer_270.__index = MetaContainer_270

function MetaContainer_270.new(val)
    return setmetatable({val = val}, MetaContainer_270)
end

MetaContainer_270.__mul = function(a, b)
    return a.val * b.val * 1
end

local objA = MetaContainer_270.new(10)
local objB = MetaContainer_270.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 270, res))
```

## Tushuntirish va Mantiq:
270-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #270 hisobi: 20
```


# 271-Topshiriq: Metatable va metametodlar arxitekturasi #271
## Topshiriq sharti:
271-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_271 = {
    tag = "META_OBJ_271",
    multiplier = 2
}
MetaContainer_271.__index = MetaContainer_271

function MetaContainer_271.new(val)
    return setmetatable({val = val}, MetaContainer_271)
end

MetaContainer_271.__mul = function(a, b)
    return a.val * b.val * 2
end

local objA = MetaContainer_271.new(10)
local objB = MetaContainer_271.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 271, res))
```

## Tushuntirish va Mantiq:
271-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #271 hisobi: 40
```


# 272-Topshiriq: Metatable va metametodlar arxitekturasi #272
## Topshiriq sharti:
272-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_272 = {
    tag = "META_OBJ_272",
    multiplier = 3
}
MetaContainer_272.__index = MetaContainer_272

function MetaContainer_272.new(val)
    return setmetatable({val = val}, MetaContainer_272)
end

MetaContainer_272.__mul = function(a, b)
    return a.val * b.val * 3
end

local objA = MetaContainer_272.new(10)
local objB = MetaContainer_272.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 272, res))
```

## Tushuntirish va Mantiq:
272-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #272 hisobi: 60
```


# 273-Topshiriq: Metatable va metametodlar arxitekturasi #273
## Topshiriq sharti:
273-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_273 = {
    tag = "META_OBJ_273",
    multiplier = 4
}
MetaContainer_273.__index = MetaContainer_273

function MetaContainer_273.new(val)
    return setmetatable({val = val}, MetaContainer_273)
end

MetaContainer_273.__mul = function(a, b)
    return a.val * b.val * 4
end

local objA = MetaContainer_273.new(10)
local objB = MetaContainer_273.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 273, res))
```

## Tushuntirish va Mantiq:
273-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #273 hisobi: 80
```


# 274-Topshiriq: Metatable va metametodlar arxitekturasi #274
## Topshiriq sharti:
274-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_274 = {
    tag = "META_OBJ_274",
    multiplier = 5
}
MetaContainer_274.__index = MetaContainer_274

function MetaContainer_274.new(val)
    return setmetatable({val = val}, MetaContainer_274)
end

MetaContainer_274.__mul = function(a, b)
    return a.val * b.val * 5
end

local objA = MetaContainer_274.new(10)
local objB = MetaContainer_274.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 274, res))
```

## Tushuntirish va Mantiq:
274-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #274 hisobi: 100
```


# 275-Topshiriq: Metatable va metametodlar arxitekturasi #275
## Topshiriq sharti:
275-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_275 = {
    tag = "META_OBJ_275",
    multiplier = 6
}
MetaContainer_275.__index = MetaContainer_275

function MetaContainer_275.new(val)
    return setmetatable({val = val}, MetaContainer_275)
end

MetaContainer_275.__mul = function(a, b)
    return a.val * b.val * 1
end

local objA = MetaContainer_275.new(10)
local objB = MetaContainer_275.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 275, res))
```

## Tushuntirish va Mantiq:
275-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #275 hisobi: 20
```


# 276-Topshiriq: Metatable va metametodlar arxitekturasi #276
## Topshiriq sharti:
276-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_276 = {
    tag = "META_OBJ_276",
    multiplier = 7
}
MetaContainer_276.__index = MetaContainer_276

function MetaContainer_276.new(val)
    return setmetatable({val = val}, MetaContainer_276)
end

MetaContainer_276.__mul = function(a, b)
    return a.val * b.val * 2
end

local objA = MetaContainer_276.new(10)
local objB = MetaContainer_276.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 276, res))
```

## Tushuntirish va Mantiq:
276-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #276 hisobi: 40
```


# 277-Topshiriq: Metatable va metametodlar arxitekturasi #277
## Topshiriq sharti:
277-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_277 = {
    tag = "META_OBJ_277",
    multiplier = 8
}
MetaContainer_277.__index = MetaContainer_277

function MetaContainer_277.new(val)
    return setmetatable({val = val}, MetaContainer_277)
end

MetaContainer_277.__mul = function(a, b)
    return a.val * b.val * 3
end

local objA = MetaContainer_277.new(10)
local objB = MetaContainer_277.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 277, res))
```

## Tushuntirish va Mantiq:
277-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #277 hisobi: 60
```


# 278-Topshiriq: Metatable va metametodlar arxitekturasi #278
## Topshiriq sharti:
278-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_278 = {
    tag = "META_OBJ_278",
    multiplier = 9
}
MetaContainer_278.__index = MetaContainer_278

function MetaContainer_278.new(val)
    return setmetatable({val = val}, MetaContainer_278)
end

MetaContainer_278.__mul = function(a, b)
    return a.val * b.val * 4
end

local objA = MetaContainer_278.new(10)
local objB = MetaContainer_278.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 278, res))
```

## Tushuntirish va Mantiq:
278-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #278 hisobi: 80
```


# 279-Topshiriq: Metatable va metametodlar arxitekturasi #279
## Topshiriq sharti:
279-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_279 = {
    tag = "META_OBJ_279",
    multiplier = 10
}
MetaContainer_279.__index = MetaContainer_279

function MetaContainer_279.new(val)
    return setmetatable({val = val}, MetaContainer_279)
end

MetaContainer_279.__mul = function(a, b)
    return a.val * b.val * 5
end

local objA = MetaContainer_279.new(10)
local objB = MetaContainer_279.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 279, res))
```

## Tushuntirish va Mantiq:
279-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #279 hisobi: 100
```


# 280-Topshiriq: Metatable va metametodlar arxitekturasi #280
## Topshiriq sharti:
280-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_280 = {
    tag = "META_OBJ_280",
    multiplier = 1
}
MetaContainer_280.__index = MetaContainer_280

function MetaContainer_280.new(val)
    return setmetatable({val = val}, MetaContainer_280)
end

MetaContainer_280.__mul = function(a, b)
    return a.val * b.val * 1
end

local objA = MetaContainer_280.new(10)
local objB = MetaContainer_280.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 280, res))
```

## Tushuntirish va Mantiq:
280-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #280 hisobi: 20
```


# 281-Topshiriq: Metatable va metametodlar arxitekturasi #281
## Topshiriq sharti:
281-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_281 = {
    tag = "META_OBJ_281",
    multiplier = 2
}
MetaContainer_281.__index = MetaContainer_281

function MetaContainer_281.new(val)
    return setmetatable({val = val}, MetaContainer_281)
end

MetaContainer_281.__mul = function(a, b)
    return a.val * b.val * 2
end

local objA = MetaContainer_281.new(10)
local objB = MetaContainer_281.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 281, res))
```

## Tushuntirish va Mantiq:
281-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #281 hisobi: 40
```


# 282-Topshiriq: Metatable va metametodlar arxitekturasi #282
## Topshiriq sharti:
282-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_282 = {
    tag = "META_OBJ_282",
    multiplier = 3
}
MetaContainer_282.__index = MetaContainer_282

function MetaContainer_282.new(val)
    return setmetatable({val = val}, MetaContainer_282)
end

MetaContainer_282.__mul = function(a, b)
    return a.val * b.val * 3
end

local objA = MetaContainer_282.new(10)
local objB = MetaContainer_282.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 282, res))
```

## Tushuntirish va Mantiq:
282-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #282 hisobi: 60
```


# 283-Topshiriq: Metatable va metametodlar arxitekturasi #283
## Topshiriq sharti:
283-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_283 = {
    tag = "META_OBJ_283",
    multiplier = 4
}
MetaContainer_283.__index = MetaContainer_283

function MetaContainer_283.new(val)
    return setmetatable({val = val}, MetaContainer_283)
end

MetaContainer_283.__mul = function(a, b)
    return a.val * b.val * 4
end

local objA = MetaContainer_283.new(10)
local objB = MetaContainer_283.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 283, res))
```

## Tushuntirish va Mantiq:
283-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #283 hisobi: 80
```


# 284-Topshiriq: Metatable va metametodlar arxitekturasi #284
## Topshiriq sharti:
284-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_284 = {
    tag = "META_OBJ_284",
    multiplier = 5
}
MetaContainer_284.__index = MetaContainer_284

function MetaContainer_284.new(val)
    return setmetatable({val = val}, MetaContainer_284)
end

MetaContainer_284.__mul = function(a, b)
    return a.val * b.val * 5
end

local objA = MetaContainer_284.new(10)
local objB = MetaContainer_284.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 284, res))
```

## Tushuntirish va Mantiq:
284-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #284 hisobi: 100
```


# 285-Topshiriq: Metatable va metametodlar arxitekturasi #285
## Topshiriq sharti:
285-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_285 = {
    tag = "META_OBJ_285",
    multiplier = 6
}
MetaContainer_285.__index = MetaContainer_285

function MetaContainer_285.new(val)
    return setmetatable({val = val}, MetaContainer_285)
end

MetaContainer_285.__mul = function(a, b)
    return a.val * b.val * 1
end

local objA = MetaContainer_285.new(10)
local objB = MetaContainer_285.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 285, res))
```

## Tushuntirish va Mantiq:
285-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #285 hisobi: 20
```


# 286-Topshiriq: Metatable va metametodlar arxitekturasi #286
## Topshiriq sharti:
286-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_286 = {
    tag = "META_OBJ_286",
    multiplier = 7
}
MetaContainer_286.__index = MetaContainer_286

function MetaContainer_286.new(val)
    return setmetatable({val = val}, MetaContainer_286)
end

MetaContainer_286.__mul = function(a, b)
    return a.val * b.val * 2
end

local objA = MetaContainer_286.new(10)
local objB = MetaContainer_286.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 286, res))
```

## Tushuntirish va Mantiq:
286-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #286 hisobi: 40
```


# 287-Topshiriq: Metatable va metametodlar arxitekturasi #287
## Topshiriq sharti:
287-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_287 = {
    tag = "META_OBJ_287",
    multiplier = 8
}
MetaContainer_287.__index = MetaContainer_287

function MetaContainer_287.new(val)
    return setmetatable({val = val}, MetaContainer_287)
end

MetaContainer_287.__mul = function(a, b)
    return a.val * b.val * 3
end

local objA = MetaContainer_287.new(10)
local objB = MetaContainer_287.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 287, res))
```

## Tushuntirish va Mantiq:
287-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #287 hisobi: 60
```


# 288-Topshiriq: Metatable va metametodlar arxitekturasi #288
## Topshiriq sharti:
288-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_288 = {
    tag = "META_OBJ_288",
    multiplier = 9
}
MetaContainer_288.__index = MetaContainer_288

function MetaContainer_288.new(val)
    return setmetatable({val = val}, MetaContainer_288)
end

MetaContainer_288.__mul = function(a, b)
    return a.val * b.val * 4
end

local objA = MetaContainer_288.new(10)
local objB = MetaContainer_288.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 288, res))
```

## Tushuntirish va Mantiq:
288-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #288 hisobi: 80
```


# 289-Topshiriq: Metatable va metametodlar arxitekturasi #289
## Topshiriq sharti:
289-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_289 = {
    tag = "META_OBJ_289",
    multiplier = 10
}
MetaContainer_289.__index = MetaContainer_289

function MetaContainer_289.new(val)
    return setmetatable({val = val}, MetaContainer_289)
end

MetaContainer_289.__mul = function(a, b)
    return a.val * b.val * 5
end

local objA = MetaContainer_289.new(10)
local objB = MetaContainer_289.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 289, res))
```

## Tushuntirish va Mantiq:
289-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #289 hisobi: 100
```


# 290-Topshiriq: Metatable va metametodlar arxitekturasi #290
## Topshiriq sharti:
290-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_290 = {
    tag = "META_OBJ_290",
    multiplier = 1
}
MetaContainer_290.__index = MetaContainer_290

function MetaContainer_290.new(val)
    return setmetatable({val = val}, MetaContainer_290)
end

MetaContainer_290.__mul = function(a, b)
    return a.val * b.val * 1
end

local objA = MetaContainer_290.new(10)
local objB = MetaContainer_290.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 290, res))
```

## Tushuntirish va Mantiq:
290-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #290 hisobi: 20
```


# 291-Topshiriq: Metatable va metametodlar arxitekturasi #291
## Topshiriq sharti:
291-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_291 = {
    tag = "META_OBJ_291",
    multiplier = 2
}
MetaContainer_291.__index = MetaContainer_291

function MetaContainer_291.new(val)
    return setmetatable({val = val}, MetaContainer_291)
end

MetaContainer_291.__mul = function(a, b)
    return a.val * b.val * 2
end

local objA = MetaContainer_291.new(10)
local objB = MetaContainer_291.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 291, res))
```

## Tushuntirish va Mantiq:
291-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #291 hisobi: 40
```


# 292-Topshiriq: Metatable va metametodlar arxitekturasi #292
## Topshiriq sharti:
292-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_292 = {
    tag = "META_OBJ_292",
    multiplier = 3
}
MetaContainer_292.__index = MetaContainer_292

function MetaContainer_292.new(val)
    return setmetatable({val = val}, MetaContainer_292)
end

MetaContainer_292.__mul = function(a, b)
    return a.val * b.val * 3
end

local objA = MetaContainer_292.new(10)
local objB = MetaContainer_292.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 292, res))
```

## Tushuntirish va Mantiq:
292-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #292 hisobi: 60
```


# 293-Topshiriq: Metatable va metametodlar arxitekturasi #293
## Topshiriq sharti:
293-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_293 = {
    tag = "META_OBJ_293",
    multiplier = 4
}
MetaContainer_293.__index = MetaContainer_293

function MetaContainer_293.new(val)
    return setmetatable({val = val}, MetaContainer_293)
end

MetaContainer_293.__mul = function(a, b)
    return a.val * b.val * 4
end

local objA = MetaContainer_293.new(10)
local objB = MetaContainer_293.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 293, res))
```

## Tushuntirish va Mantiq:
293-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #293 hisobi: 80
```


# 294-Topshiriq: Metatable va metametodlar arxitekturasi #294
## Topshiriq sharti:
294-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_294 = {
    tag = "META_OBJ_294",
    multiplier = 5
}
MetaContainer_294.__index = MetaContainer_294

function MetaContainer_294.new(val)
    return setmetatable({val = val}, MetaContainer_294)
end

MetaContainer_294.__mul = function(a, b)
    return a.val * b.val * 5
end

local objA = MetaContainer_294.new(10)
local objB = MetaContainer_294.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 294, res))
```

## Tushuntirish va Mantiq:
294-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #294 hisobi: 100
```


# 295-Topshiriq: Metatable va metametodlar arxitekturasi #295
## Topshiriq sharti:
295-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_295 = {
    tag = "META_OBJ_295",
    multiplier = 6
}
MetaContainer_295.__index = MetaContainer_295

function MetaContainer_295.new(val)
    return setmetatable({val = val}, MetaContainer_295)
end

MetaContainer_295.__mul = function(a, b)
    return a.val * b.val * 1
end

local objA = MetaContainer_295.new(10)
local objB = MetaContainer_295.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 295, res))
```

## Tushuntirish va Mantiq:
295-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #295 hisobi: 20
```


# 296-Topshiriq: Metatable va metametodlar arxitekturasi #296
## Topshiriq sharti:
296-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_296 = {
    tag = "META_OBJ_296",
    multiplier = 7
}
MetaContainer_296.__index = MetaContainer_296

function MetaContainer_296.new(val)
    return setmetatable({val = val}, MetaContainer_296)
end

MetaContainer_296.__mul = function(a, b)
    return a.val * b.val * 2
end

local objA = MetaContainer_296.new(10)
local objB = MetaContainer_296.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 296, res))
```

## Tushuntirish va Mantiq:
296-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #296 hisobi: 40
```


# 297-Topshiriq: Metatable va metametodlar arxitekturasi #297
## Topshiriq sharti:
297-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_297 = {
    tag = "META_OBJ_297",
    multiplier = 8
}
MetaContainer_297.__index = MetaContainer_297

function MetaContainer_297.new(val)
    return setmetatable({val = val}, MetaContainer_297)
end

MetaContainer_297.__mul = function(a, b)
    return a.val * b.val * 3
end

local objA = MetaContainer_297.new(10)
local objB = MetaContainer_297.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 297, res))
```

## Tushuntirish va Mantiq:
297-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #297 hisobi: 60
```


# 298-Topshiriq: Metatable va metametodlar arxitekturasi #298
## Topshiriq sharti:
298-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_298 = {
    tag = "META_OBJ_298",
    multiplier = 9
}
MetaContainer_298.__index = MetaContainer_298

function MetaContainer_298.new(val)
    return setmetatable({val = val}, MetaContainer_298)
end

MetaContainer_298.__mul = function(a, b)
    return a.val * b.val * 4
end

local objA = MetaContainer_298.new(10)
local objB = MetaContainer_298.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 298, res))
```

## Tushuntirish va Mantiq:
298-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #298 hisobi: 80
```


# 299-Topshiriq: Metatable va metametodlar arxitekturasi #299
## Topshiriq sharti:
299-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_299 = {
    tag = "META_OBJ_299",
    multiplier = 10
}
MetaContainer_299.__index = MetaContainer_299

function MetaContainer_299.new(val)
    return setmetatable({val = val}, MetaContainer_299)
end

MetaContainer_299.__mul = function(a, b)
    return a.val * b.val * 5
end

local objA = MetaContainer_299.new(10)
local objB = MetaContainer_299.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 299, res))
```

## Tushuntirish va Mantiq:
299-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #299 hisobi: 100
```


# 300-Topshiriq: Metatable va metametodlar arxitekturasi #300
## Topshiriq sharti:
300-vazifa: Metatable mexanizmlari, operatorlarni qayta yuklash va maxsus semantikani shakllantirish.

## Yechim (Lua kodi):
```lua
local MetaContainer_300 = {
    tag = "META_OBJ_300",
    multiplier = 1
}
MetaContainer_300.__index = MetaContainer_300

function MetaContainer_300.new(val)
    return setmetatable({val = val}, MetaContainer_300)
end

MetaContainer_300.__mul = function(a, b)
    return a.val * b.val * 1
end

local objA = MetaContainer_300.new(10)
local objB = MetaContainer_300.new(2)
local res = objA * objB
print(string.format("Meta ob'ekt #%d hisobi: %d", 300, res))
```

## Tushuntirish va Mantiq:
300-vazifada maxsus `__mul` va `__index` metametodlari orqali matematik operatsiyalar nazorat qilindi.

## Ishlash natijasi:
```text
Meta ob'ekt #300 hisobi: 20
```

