# 301-Topshiriq: Prototipga asoslangan sinf e'lon qilish va :new() konstruktori
## Topshiriq sharti:
O'yin personaji (Character) sinfini yaratib undan instansiyalar oling.

## Yechim (Lua kodi):
```lua
local Character = {}
Character.__index = Character

function Character:new(name, role)
    local instance = setmetatable({}, Character)
    instance.name = name
    instance.role = role
    return instance
end

function Character:introduce()
    print("Salom! Men " .. self.name .. ", kasbim: " .. self.role)
end

local hero = Character:new("Rustam", "Mergan")
hero:introduce()
```

## Tushuntirish va Mantiq:
Lua tilida klassik sinflar yo'q, ularning o'rniga jadvallar prototip sifatida xizmat qiladi. `Character.__index = Character` orqali yangi instansiyalar metodlarni ota jadvaldan meros oladi.

## Ishlash natijasi:
```text
Salom! Men Rustam, kasbim: Mergan
```


# 302-Topshiriq: Nuqta (.) va ikki nuqta (:) metod sintaksisi tafovuti
## Topshiriq sharti:
Metodlarni nuqta va ikki nuqta orqali chaqirib, 'self' ning qanday uzatilishini ko'rsating.

## Yechim (Lua kodi):
```lua
local Calculator = {value = 100}

function Calculator:add(n)
    self.value = self.value + n
end

-- Ikki nuqta bilan chaqirish:
Calculator:add(50)
print("Qiymat: " .. Calculator.value)

-- Nuqta bilan chaqirish (self qo'lda uzatiladi):
Calculator.add(Calculator, 25)
print("Yangi qiymat: " .. Calculator.value)
```

## Tushuntirish va Mantiq:
`obj:method(...)` sintaksisi `obj.method(obj, ...)` bilan 100% bir xil bo'lib, 'self' ko'rsatkichini birinchi parametr qilib yashirin uzatadi.

## Ishlash natijasi:
```text
Qiymat: 150
Yangi qiymat: 175
```


# 303-Topshiriq: Yagona merosxo'rlik (Single Inheritance)
## Topshiriq sharti:
Base sinfdan (Vehicle) meros oluvchi Car sinfini yarating va metodlarni kengaytiring.

## Yechim (Lua kodi):
```lua
local Vehicle = {}
Vehicle.__index = Vehicle

function Vehicle:new(brand)
    local self = setmetatable({}, self)
    self.brand = brand
    return self
end

function Vehicle:move()
    print(self.brand .. " harakatlanmoqda...")
end

-- Meros olish:
local Car = setmetatable({}, {__index = Vehicle})
Car.__index = Car

function Car:new(brand, speed)
    local self = Vehicle.new(self, brand)
    self.speed = speed
    return self
end

function Car:honk()
    print(self.brand .. " signal chaldi: Bip-bip! Tezligi: " .. self.speed .. " km/s")
end

local myCar = Car:new("Chevrolet", 180)
myCar:move()
myCar:honk()
```

## Tushuntirish va Mantiq:
Merosxo'rlik bolalar sinfining metatable `__index` ini ota sinfga bog'lash orqali hosil qilinadi.

## Ishlash natijasi:
```text
Chevrolet harakatlanmoqda...
Chevrolet signal chaldi: Bip-bip! Tezligi: 180 km/s
```


# 304-Topshiriq: Metodni qayta yozish (Method Overriding) va Super chaqiruvi
## Topshiriq sharti:
Bolalar sinfida ota metodni qayta yozing va uning asl variantini ham chaqiring.

## Yechim (Lua kodi):
```lua
local Animal = {}
Animal.__index = Animal

function Animal:new(name)
    return setmetatable({name = name}, self)
end

function Animal:speak()
    return self.name .. " ovoz chiqaradi"
end

local Dog = setmetatable({}, {__index = Animal})
Dog.__index = Dog

function Dog:speak()
    local parentVoice = Animal.speak(self)
    return parentVoice .. " -> Vov-vov!"
end

local d = Dog:new("To'rtko'z")
print(d:speak())
```

## Tushuntirish va Mantiq:
Overridingda ota sinf metodiga `ParentClass.method(self)` ko'rinishida murojaat qilib super chaqiruvi amalga oshiriladi.

## Ishlash natijasi:
```text
To'rtko'z ovoz chiqaradi -> Vov-vov!
```


# 305-Topshiriq: Polimorfizm amaliyoti
## Topshiriq sharti:
Turli sinf instansiyalarini umumiy interfeys orqali bitta tsiklda boshqaring.

## Yechim (Lua kodi):
```lua
local shapes = {
    {area = function() return 25 end, name = "Kvadrat"},
    {area = function() return 50 end, name = "To'g'ri to'rtburchak"},
    {area = function() return 78.5 end, name = "Doira"}
}

for _, shape in ipairs(shapes) do
    print(string.format("%-20s yuzasi: %.1f", shape.name, shape.area()))
end
```

## Tushuntirish va Mantiq:
Duck typing va polimorfizm Luada tabiiy bo'lib, ob'ektning metodi mavjud bo'lsa, u muvaffaqiyatli ishlaydi.

## Ishlash natijasi:
```text
Kvadrat              yuzasi: 25.0
To'g'ri to'rtburchak yuzasi: 50.0
Doira                yuzasi: 78.5
```


# 306-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #306
## Topshiriq sharti:
306-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_306 = {}
Component_306.__index = Component_306

function Component_306:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 306
    return inst
end

function Component_306:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 306, self.name, self.power)
end

local comp = Component_306:new("Sensor", 918)
print(comp:status())
```

## Tushuntirish va Mantiq:
306-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #306: 'Sensor' (Quvvat: 918)
```


# 307-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #307
## Topshiriq sharti:
307-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_307 = {}
Component_307.__index = Component_307

function Component_307:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 307
    return inst
end

function Component_307:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 307, self.name, self.power)
end

local comp = Component_307:new("Sensor", 921)
print(comp:status())
```

## Tushuntirish va Mantiq:
307-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #307: 'Sensor' (Quvvat: 921)
```


# 308-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #308
## Topshiriq sharti:
308-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_308 = {}
Component_308.__index = Component_308

function Component_308:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 308
    return inst
end

function Component_308:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 308, self.name, self.power)
end

local comp = Component_308:new("Sensor", 924)
print(comp:status())
```

## Tushuntirish va Mantiq:
308-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #308: 'Sensor' (Quvvat: 924)
```


# 309-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #309
## Topshiriq sharti:
309-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_309 = {}
Component_309.__index = Component_309

function Component_309:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 309
    return inst
end

function Component_309:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 309, self.name, self.power)
end

local comp = Component_309:new("Sensor", 927)
print(comp:status())
```

## Tushuntirish va Mantiq:
309-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #309: 'Sensor' (Quvvat: 927)
```


# 310-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #310
## Topshiriq sharti:
310-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_310 = {}
Component_310.__index = Component_310

function Component_310:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 310
    return inst
end

function Component_310:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 310, self.name, self.power)
end

local comp = Component_310:new("Sensor", 930)
print(comp:status())
```

## Tushuntirish va Mantiq:
310-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #310: 'Sensor' (Quvvat: 930)
```


# 311-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #311
## Topshiriq sharti:
311-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_311 = {}
Component_311.__index = Component_311

function Component_311:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 311
    return inst
end

function Component_311:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 311, self.name, self.power)
end

local comp = Component_311:new("Sensor", 933)
print(comp:status())
```

## Tushuntirish va Mantiq:
311-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #311: 'Sensor' (Quvvat: 933)
```


# 312-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #312
## Topshiriq sharti:
312-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_312 = {}
Component_312.__index = Component_312

function Component_312:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 312
    return inst
end

function Component_312:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 312, self.name, self.power)
end

local comp = Component_312:new("Sensor", 936)
print(comp:status())
```

## Tushuntirish va Mantiq:
312-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #312: 'Sensor' (Quvvat: 936)
```


# 313-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #313
## Topshiriq sharti:
313-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_313 = {}
Component_313.__index = Component_313

function Component_313:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 313
    return inst
end

function Component_313:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 313, self.name, self.power)
end

local comp = Component_313:new("Sensor", 939)
print(comp:status())
```

## Tushuntirish va Mantiq:
313-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #313: 'Sensor' (Quvvat: 939)
```


# 314-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #314
## Topshiriq sharti:
314-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_314 = {}
Component_314.__index = Component_314

function Component_314:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 314
    return inst
end

function Component_314:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 314, self.name, self.power)
end

local comp = Component_314:new("Sensor", 942)
print(comp:status())
```

## Tushuntirish va Mantiq:
314-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #314: 'Sensor' (Quvvat: 942)
```


# 315-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #315
## Topshiriq sharti:
315-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_315 = {}
Component_315.__index = Component_315

function Component_315:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 315
    return inst
end

function Component_315:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 315, self.name, self.power)
end

local comp = Component_315:new("Sensor", 945)
print(comp:status())
```

## Tushuntirish va Mantiq:
315-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #315: 'Sensor' (Quvvat: 945)
```


# 316-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #316
## Topshiriq sharti:
316-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_316 = {}
Component_316.__index = Component_316

function Component_316:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 316
    return inst
end

function Component_316:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 316, self.name, self.power)
end

local comp = Component_316:new("Sensor", 948)
print(comp:status())
```

## Tushuntirish va Mantiq:
316-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #316: 'Sensor' (Quvvat: 948)
```


# 317-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #317
## Topshiriq sharti:
317-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_317 = {}
Component_317.__index = Component_317

function Component_317:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 317
    return inst
end

function Component_317:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 317, self.name, self.power)
end

local comp = Component_317:new("Sensor", 951)
print(comp:status())
```

## Tushuntirish va Mantiq:
317-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #317: 'Sensor' (Quvvat: 951)
```


# 318-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #318
## Topshiriq sharti:
318-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_318 = {}
Component_318.__index = Component_318

function Component_318:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 318
    return inst
end

function Component_318:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 318, self.name, self.power)
end

local comp = Component_318:new("Sensor", 954)
print(comp:status())
```

## Tushuntirish va Mantiq:
318-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #318: 'Sensor' (Quvvat: 954)
```


# 319-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #319
## Topshiriq sharti:
319-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_319 = {}
Component_319.__index = Component_319

function Component_319:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 319
    return inst
end

function Component_319:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 319, self.name, self.power)
end

local comp = Component_319:new("Sensor", 957)
print(comp:status())
```

## Tushuntirish va Mantiq:
319-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #319: 'Sensor' (Quvvat: 957)
```


# 320-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #320
## Topshiriq sharti:
320-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_320 = {}
Component_320.__index = Component_320

function Component_320:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 320
    return inst
end

function Component_320:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 320, self.name, self.power)
end

local comp = Component_320:new("Sensor", 960)
print(comp:status())
```

## Tushuntirish va Mantiq:
320-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #320: 'Sensor' (Quvvat: 960)
```


# 321-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #321
## Topshiriq sharti:
321-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_321 = {}
Component_321.__index = Component_321

function Component_321:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 321
    return inst
end

function Component_321:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 321, self.name, self.power)
end

local comp = Component_321:new("Sensor", 963)
print(comp:status())
```

## Tushuntirish va Mantiq:
321-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #321: 'Sensor' (Quvvat: 963)
```


# 322-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #322
## Topshiriq sharti:
322-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_322 = {}
Component_322.__index = Component_322

function Component_322:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 322
    return inst
end

function Component_322:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 322, self.name, self.power)
end

local comp = Component_322:new("Sensor", 966)
print(comp:status())
```

## Tushuntirish va Mantiq:
322-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #322: 'Sensor' (Quvvat: 966)
```


# 323-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #323
## Topshiriq sharti:
323-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_323 = {}
Component_323.__index = Component_323

function Component_323:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 323
    return inst
end

function Component_323:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 323, self.name, self.power)
end

local comp = Component_323:new("Sensor", 969)
print(comp:status())
```

## Tushuntirish va Mantiq:
323-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #323: 'Sensor' (Quvvat: 969)
```


# 324-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #324
## Topshiriq sharti:
324-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_324 = {}
Component_324.__index = Component_324

function Component_324:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 324
    return inst
end

function Component_324:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 324, self.name, self.power)
end

local comp = Component_324:new("Sensor", 972)
print(comp:status())
```

## Tushuntirish va Mantiq:
324-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #324: 'Sensor' (Quvvat: 972)
```


# 325-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #325
## Topshiriq sharti:
325-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_325 = {}
Component_325.__index = Component_325

function Component_325:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 325
    return inst
end

function Component_325:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 325, self.name, self.power)
end

local comp = Component_325:new("Sensor", 975)
print(comp:status())
```

## Tushuntirish va Mantiq:
325-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #325: 'Sensor' (Quvvat: 975)
```


# 326-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #326
## Topshiriq sharti:
326-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_326 = {}
Component_326.__index = Component_326

function Component_326:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 326
    return inst
end

function Component_326:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 326, self.name, self.power)
end

local comp = Component_326:new("Sensor", 978)
print(comp:status())
```

## Tushuntirish va Mantiq:
326-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #326: 'Sensor' (Quvvat: 978)
```


# 327-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #327
## Topshiriq sharti:
327-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_327 = {}
Component_327.__index = Component_327

function Component_327:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 327
    return inst
end

function Component_327:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 327, self.name, self.power)
end

local comp = Component_327:new("Sensor", 981)
print(comp:status())
```

## Tushuntirish va Mantiq:
327-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #327: 'Sensor' (Quvvat: 981)
```


# 328-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #328
## Topshiriq sharti:
328-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_328 = {}
Component_328.__index = Component_328

function Component_328:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 328
    return inst
end

function Component_328:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 328, self.name, self.power)
end

local comp = Component_328:new("Sensor", 984)
print(comp:status())
```

## Tushuntirish va Mantiq:
328-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #328: 'Sensor' (Quvvat: 984)
```


# 329-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #329
## Topshiriq sharti:
329-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_329 = {}
Component_329.__index = Component_329

function Component_329:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 329
    return inst
end

function Component_329:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 329, self.name, self.power)
end

local comp = Component_329:new("Sensor", 987)
print(comp:status())
```

## Tushuntirish va Mantiq:
329-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #329: 'Sensor' (Quvvat: 987)
```


# 330-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #330
## Topshiriq sharti:
330-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_330 = {}
Component_330.__index = Component_330

function Component_330:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 330
    return inst
end

function Component_330:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 330, self.name, self.power)
end

local comp = Component_330:new("Sensor", 990)
print(comp:status())
```

## Tushuntirish va Mantiq:
330-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #330: 'Sensor' (Quvvat: 990)
```


# 331-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #331
## Topshiriq sharti:
331-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_331 = {}
Component_331.__index = Component_331

function Component_331:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 331
    return inst
end

function Component_331:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 331, self.name, self.power)
end

local comp = Component_331:new("Sensor", 993)
print(comp:status())
```

## Tushuntirish va Mantiq:
331-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #331: 'Sensor' (Quvvat: 993)
```


# 332-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #332
## Topshiriq sharti:
332-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_332 = {}
Component_332.__index = Component_332

function Component_332:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 332
    return inst
end

function Component_332:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 332, self.name, self.power)
end

local comp = Component_332:new("Sensor", 996)
print(comp:status())
```

## Tushuntirish va Mantiq:
332-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #332: 'Sensor' (Quvvat: 996)
```


# 333-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #333
## Topshiriq sharti:
333-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_333 = {}
Component_333.__index = Component_333

function Component_333:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 333
    return inst
end

function Component_333:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 333, self.name, self.power)
end

local comp = Component_333:new("Sensor", 999)
print(comp:status())
```

## Tushuntirish va Mantiq:
333-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #333: 'Sensor' (Quvvat: 999)
```


# 334-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #334
## Topshiriq sharti:
334-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_334 = {}
Component_334.__index = Component_334

function Component_334:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 334
    return inst
end

function Component_334:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 334, self.name, self.power)
end

local comp = Component_334:new("Sensor", 1002)
print(comp:status())
```

## Tushuntirish va Mantiq:
334-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #334: 'Sensor' (Quvvat: 1002)
```


# 335-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #335
## Topshiriq sharti:
335-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_335 = {}
Component_335.__index = Component_335

function Component_335:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 335
    return inst
end

function Component_335:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 335, self.name, self.power)
end

local comp = Component_335:new("Sensor", 1005)
print(comp:status())
```

## Tushuntirish va Mantiq:
335-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #335: 'Sensor' (Quvvat: 1005)
```


# 336-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #336
## Topshiriq sharti:
336-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_336 = {}
Component_336.__index = Component_336

function Component_336:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 336
    return inst
end

function Component_336:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 336, self.name, self.power)
end

local comp = Component_336:new("Sensor", 1008)
print(comp:status())
```

## Tushuntirish va Mantiq:
336-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #336: 'Sensor' (Quvvat: 1008)
```


# 337-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #337
## Topshiriq sharti:
337-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_337 = {}
Component_337.__index = Component_337

function Component_337:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 337
    return inst
end

function Component_337:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 337, self.name, self.power)
end

local comp = Component_337:new("Sensor", 1011)
print(comp:status())
```

## Tushuntirish va Mantiq:
337-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #337: 'Sensor' (Quvvat: 1011)
```


# 338-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #338
## Topshiriq sharti:
338-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_338 = {}
Component_338.__index = Component_338

function Component_338:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 338
    return inst
end

function Component_338:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 338, self.name, self.power)
end

local comp = Component_338:new("Sensor", 1014)
print(comp:status())
```

## Tushuntirish va Mantiq:
338-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #338: 'Sensor' (Quvvat: 1014)
```


# 339-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #339
## Topshiriq sharti:
339-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_339 = {}
Component_339.__index = Component_339

function Component_339:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 339
    return inst
end

function Component_339:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 339, self.name, self.power)
end

local comp = Component_339:new("Sensor", 1017)
print(comp:status())
```

## Tushuntirish va Mantiq:
339-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #339: 'Sensor' (Quvvat: 1017)
```


# 340-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #340
## Topshiriq sharti:
340-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_340 = {}
Component_340.__index = Component_340

function Component_340:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 340
    return inst
end

function Component_340:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 340, self.name, self.power)
end

local comp = Component_340:new("Sensor", 1020)
print(comp:status())
```

## Tushuntirish va Mantiq:
340-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #340: 'Sensor' (Quvvat: 1020)
```


# 341-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #341
## Topshiriq sharti:
341-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_341 = {}
Component_341.__index = Component_341

function Component_341:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 341
    return inst
end

function Component_341:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 341, self.name, self.power)
end

local comp = Component_341:new("Sensor", 1023)
print(comp:status())
```

## Tushuntirish va Mantiq:
341-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #341: 'Sensor' (Quvvat: 1023)
```


# 342-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #342
## Topshiriq sharti:
342-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_342 = {}
Component_342.__index = Component_342

function Component_342:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 342
    return inst
end

function Component_342:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 342, self.name, self.power)
end

local comp = Component_342:new("Sensor", 1026)
print(comp:status())
```

## Tushuntirish va Mantiq:
342-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #342: 'Sensor' (Quvvat: 1026)
```


# 343-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #343
## Topshiriq sharti:
343-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_343 = {}
Component_343.__index = Component_343

function Component_343:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 343
    return inst
end

function Component_343:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 343, self.name, self.power)
end

local comp = Component_343:new("Sensor", 1029)
print(comp:status())
```

## Tushuntirish va Mantiq:
343-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #343: 'Sensor' (Quvvat: 1029)
```


# 344-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #344
## Topshiriq sharti:
344-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_344 = {}
Component_344.__index = Component_344

function Component_344:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 344
    return inst
end

function Component_344:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 344, self.name, self.power)
end

local comp = Component_344:new("Sensor", 1032)
print(comp:status())
```

## Tushuntirish va Mantiq:
344-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #344: 'Sensor' (Quvvat: 1032)
```


# 345-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #345
## Topshiriq sharti:
345-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_345 = {}
Component_345.__index = Component_345

function Component_345:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 345
    return inst
end

function Component_345:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 345, self.name, self.power)
end

local comp = Component_345:new("Sensor", 1035)
print(comp:status())
```

## Tushuntirish va Mantiq:
345-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #345: 'Sensor' (Quvvat: 1035)
```


# 346-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #346
## Topshiriq sharti:
346-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_346 = {}
Component_346.__index = Component_346

function Component_346:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 346
    return inst
end

function Component_346:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 346, self.name, self.power)
end

local comp = Component_346:new("Sensor", 1038)
print(comp:status())
```

## Tushuntirish va Mantiq:
346-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #346: 'Sensor' (Quvvat: 1038)
```


# 347-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #347
## Topshiriq sharti:
347-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_347 = {}
Component_347.__index = Component_347

function Component_347:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 347
    return inst
end

function Component_347:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 347, self.name, self.power)
end

local comp = Component_347:new("Sensor", 1041)
print(comp:status())
```

## Tushuntirish va Mantiq:
347-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #347: 'Sensor' (Quvvat: 1041)
```


# 348-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #348
## Topshiriq sharti:
348-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_348 = {}
Component_348.__index = Component_348

function Component_348:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 348
    return inst
end

function Component_348:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 348, self.name, self.power)
end

local comp = Component_348:new("Sensor", 1044)
print(comp:status())
```

## Tushuntirish va Mantiq:
348-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #348: 'Sensor' (Quvvat: 1044)
```


# 349-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #349
## Topshiriq sharti:
349-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_349 = {}
Component_349.__index = Component_349

function Component_349:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 349
    return inst
end

function Component_349:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 349, self.name, self.power)
end

local comp = Component_349:new("Sensor", 1047)
print(comp:status())
```

## Tushuntirish va Mantiq:
349-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #349: 'Sensor' (Quvvat: 1047)
```


# 350-Topshiriq: Ob'ektga yo'naltirilgan dasturlash (OOP) modeli #350
## Topshiriq sharti:
350-vazifa: Prototipga asoslangan sinf tuzilishi, enkapsulyatsiya, modullar va metodlar integratsiyasi.

## Yechim (Lua kodi):
```lua
local Component_350 = {}
Component_350.__index = Component_350

function Component_350:new(name, power)
    local inst = setmetatable({}, self)
    inst.name = name
    inst.power = power or 350
    return inst
end

function Component_350:status()
    return string.format("Komponent #%d: '%s' (Quvvat: %d)", 350, self.name, self.power)
end

local comp = Component_350:new("Sensor", 1050)
print(comp:status())
```

## Tushuntirish va Mantiq:
350-vazifada mustaqil konstruktor, instansiya xususiyatlari va prototip metodlari tatbiq etildi.

## Ishlash natijasi:
```text
Komponent #350: 'Sensor' (Quvvat: 1050)
```

