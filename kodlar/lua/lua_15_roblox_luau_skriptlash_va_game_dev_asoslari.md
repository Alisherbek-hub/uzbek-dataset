# 701-Topshiriq: Luau statik tiplash (Gradual Typing) sintaksisi
## Topshiriq sharti:
Luau kengaytmasidagi tur annotatsiyalarini va maxsus type alias yaratishni ko'rsating.

## Yechim (Lua kodi):
```lua
-- Luau tiplash simulyatsiyasi:
local function calculatePlayerScore(name, kills, deaths)
    local kdRatio = kills / math.max(1, deaths)
    return string.format("O'yinchi %s: K/D = %.2f", name, kdRatio)
end

print(calculatePlayerScore("Jasur", 15, 3))
```

## Tushuntirish va Mantiq:
Roblox Luau tilida `name: string`, `kills: number` kabi qat'iy tiplash imkoniyati mavjud bo'lib, xatolarni tahrirlovchidayoq aniqlaydi.

## Ishlash natijasi:
```text
O'yinchi Jasur: K/D = 5.00
```


# 702-Topshiriq: Roblox Workspace va yangi Part yaratish (Instance.new)
## Topshiriq sharti:
O'yin dunyosiga dasturiy ravishda yangi blok (Part) qo'shing va uning parametrlarini o'rnating.

## Yechim (Lua kodi):
```lua
local part = {
    Name = "SpawnPlatform",
    Size = {X = 10, Y = 1, Z = 10},
    Position = {X = 0, Y = 5, Z = 0},
    Anchored = true,
    BrickColor = "Bright blue"
}

print(string.format("Part yaratildi: '%s' [Anchored=%s, Joylashuv=(%d,%d,%d)]",
    part.Name, tostring(part.Anchored), part.Position.X, part.Position.Y, part.Position.Z))
```

## Tushuntirish va Mantiq:
`Instance.new('Part')` Robloxda yangi fizik ob'ekt yaratadi. `Anchored = true` uni gravitatsiya ta'sirida qulab tushishidan saqlaydi.

## Ishlash natijasi:
```text
Part yaratildi: 'SpawnPlatform' [Anchored=true, Joylashuv=(0,5,0)]
```


# 703-Topshiriq: Vector3 va CFrame koordinata tizimlari
## Topshiriq sharti:
3D fazoda koordinata va oriyentatsiyani (CFrame) modellashtiring.

## Yechim (Lua kodi):
```lua
local function createVector3(x, y, z)
    return {X = x, Y = y, Z = z}
end

local pos = createVector3(10, 50, -25)
print(string.format("Vector3 koordinatasi: (%.1f, %.1f, %.1f)", pos.X, pos.Y, pos.Z))
```

## Tushuntirish va Mantiq:
Robloxda `Vector3` oddiy 3D nuqta bo'lsa, `CFrame` (Coordinate Frame) ham joylashuv, ham 3D burilish burchagini o'z ichiga oladi.

## Ishlash natijasi:
```text
Vector3 koordinatasi: (10.0, 50.0, -25.0)
```


# 704-Topshiriq: Touched hodisasi (Event Listener)
## Topshiriq sharti:
Blokka boshqa jism tekkanida (masalan, tuzoq yoki lava) zarba yetkazuvchi mantiq.

## Yechim (Lua kodi):
```lua
local function onPartTouched(hitPartName)
    print("Ob'ekt bilan to'qnashuv yuz berdi: " .. hitPartName)
    if hitPartName == "HumanoidRootPart" then
        print("-> O'yinchiga 50 zarar yetkazildi!")
    end
end

onPartTouched("HumanoidRootPart")
```

## Tushuntirish va Mantiq:
`Part.Touched:Connect(function(hit) ... end)` orqali Robloxda to'qnashuv hodisalari ushlanadi.

## Ishlash natijasi:
```text
Ob'ekt bilan to'qnashuv yuz berdi: HumanoidRootPart
-> O'yinchiga 50 zarar yetkazildi!
```


# 705-Topshiriq: Server Script vs LocalScript vs ModuleScript
## Topshiriq sharti:
Roblox skriptlarining bajarilish joylari va rollarini ajrating.

## Yechim (Lua kodi):
```lua
local scriptTypes = {
    ["Server Script"] = "Serverda ishlaydi, umumiy dunyo holatini boshqaradi.",
    ["LocalScript"] = "Faqat mijoz (foydalanuvchi qurilmasi)da ishlaydi, UI va kamerani boshqaradi.",
    ["ModuleScript"] = "Har ikkala tomondan qayta chaqirilishi mumkin bo'lgan umumiy kutubxona."
}

for name, desc in pairs(scriptTypes) do
    print(string.format("[%s]: %s", name, desc))
end
```

## Tushuntirish va Mantiq:
Roblox arxitekturasida mijoz-server chegarasi qat'iy belgilangan: vizual effektlar LocalScript-da, muhim iqtisod va xaridlar Server Script-da bo'lishi shart.

## Ishlash natijasi:
```text
[Server Script]: Serverda ishlaydi, umumiy dunyo holatini boshqaradi.
[LocalScript]: Faqat mijoz (foydalanuvchi qurilmasi)da ishlaydi, UI va kamerani boshqaradi.
[ModuleScript]: Har ikkala tomondan qayta chaqirilishi mumkin bo'lgan umumiy kutubxona.
```


# 706-Topshiriq: Roblox Luau o'yin dasturlash asoslari #706
## Topshiriq sharti:
706-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_706 = {
    UserId = 1000 + 706,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_706:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_706:boostSpeed(11)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 706, newSpeed))
```

## Tushuntirish va Mantiq:
706-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #706 yangi tezligi: 27 (Boshlang'ich: 16)
```


# 707-Topshiriq: Roblox Luau o'yin dasturlash asoslari #707
## Topshiriq sharti:
707-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_707 = {
    UserId = 1000 + 707,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_707:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_707:boostSpeed(12)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 707, newSpeed))
```

## Tushuntirish va Mantiq:
707-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #707 yangi tezligi: 28 (Boshlang'ich: 16)
```


# 708-Topshiriq: Roblox Luau o'yin dasturlash asoslari #708
## Topshiriq sharti:
708-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_708 = {
    UserId = 1000 + 708,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_708:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_708:boostSpeed(13)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 708, newSpeed))
```

## Tushuntirish va Mantiq:
708-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #708 yangi tezligi: 29 (Boshlang'ich: 16)
```


# 709-Topshiriq: Roblox Luau o'yin dasturlash asoslari #709
## Topshiriq sharti:
709-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_709 = {
    UserId = 1000 + 709,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_709:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_709:boostSpeed(14)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 709, newSpeed))
```

## Tushuntirish va Mantiq:
709-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #709 yangi tezligi: 30 (Boshlang'ich: 16)
```


# 710-Topshiriq: Roblox Luau o'yin dasturlash asoslari #710
## Topshiriq sharti:
710-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_710 = {
    UserId = 1000 + 710,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_710:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_710:boostSpeed(5)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 710, newSpeed))
```

## Tushuntirish va Mantiq:
710-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #710 yangi tezligi: 21 (Boshlang'ich: 16)
```


# 711-Topshiriq: Roblox Luau o'yin dasturlash asoslari #711
## Topshiriq sharti:
711-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_711 = {
    UserId = 1000 + 711,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_711:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_711:boostSpeed(6)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 711, newSpeed))
```

## Tushuntirish va Mantiq:
711-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #711 yangi tezligi: 22 (Boshlang'ich: 16)
```


# 712-Topshiriq: Roblox Luau o'yin dasturlash asoslari #712
## Topshiriq sharti:
712-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_712 = {
    UserId = 1000 + 712,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_712:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_712:boostSpeed(7)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 712, newSpeed))
```

## Tushuntirish va Mantiq:
712-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #712 yangi tezligi: 23 (Boshlang'ich: 16)
```


# 713-Topshiriq: Roblox Luau o'yin dasturlash asoslari #713
## Topshiriq sharti:
713-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_713 = {
    UserId = 1000 + 713,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_713:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_713:boostSpeed(8)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 713, newSpeed))
```

## Tushuntirish va Mantiq:
713-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #713 yangi tezligi: 24 (Boshlang'ich: 16)
```


# 714-Topshiriq: Roblox Luau o'yin dasturlash asoslari #714
## Topshiriq sharti:
714-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_714 = {
    UserId = 1000 + 714,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_714:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_714:boostSpeed(9)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 714, newSpeed))
```

## Tushuntirish va Mantiq:
714-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #714 yangi tezligi: 25 (Boshlang'ich: 16)
```


# 715-Topshiriq: Roblox Luau o'yin dasturlash asoslari #715
## Topshiriq sharti:
715-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_715 = {
    UserId = 1000 + 715,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_715:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_715:boostSpeed(10)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 715, newSpeed))
```

## Tushuntirish va Mantiq:
715-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #715 yangi tezligi: 26 (Boshlang'ich: 16)
```


# 716-Topshiriq: Roblox Luau o'yin dasturlash asoslari #716
## Topshiriq sharti:
716-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_716 = {
    UserId = 1000 + 716,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_716:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_716:boostSpeed(11)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 716, newSpeed))
```

## Tushuntirish va Mantiq:
716-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #716 yangi tezligi: 27 (Boshlang'ich: 16)
```


# 717-Topshiriq: Roblox Luau o'yin dasturlash asoslari #717
## Topshiriq sharti:
717-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_717 = {
    UserId = 1000 + 717,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_717:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_717:boostSpeed(12)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 717, newSpeed))
```

## Tushuntirish va Mantiq:
717-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #717 yangi tezligi: 28 (Boshlang'ich: 16)
```


# 718-Topshiriq: Roblox Luau o'yin dasturlash asoslari #718
## Topshiriq sharti:
718-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_718 = {
    UserId = 1000 + 718,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_718:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_718:boostSpeed(13)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 718, newSpeed))
```

## Tushuntirish va Mantiq:
718-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #718 yangi tezligi: 29 (Boshlang'ich: 16)
```


# 719-Topshiriq: Roblox Luau o'yin dasturlash asoslari #719
## Topshiriq sharti:
719-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_719 = {
    UserId = 1000 + 719,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_719:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_719:boostSpeed(14)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 719, newSpeed))
```

## Tushuntirish va Mantiq:
719-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #719 yangi tezligi: 30 (Boshlang'ich: 16)
```


# 720-Topshiriq: Roblox Luau o'yin dasturlash asoslari #720
## Topshiriq sharti:
720-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_720 = {
    UserId = 1000 + 720,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_720:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_720:boostSpeed(5)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 720, newSpeed))
```

## Tushuntirish va Mantiq:
720-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #720 yangi tezligi: 21 (Boshlang'ich: 16)
```


# 721-Topshiriq: Roblox Luau o'yin dasturlash asoslari #721
## Topshiriq sharti:
721-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_721 = {
    UserId = 1000 + 721,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_721:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_721:boostSpeed(6)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 721, newSpeed))
```

## Tushuntirish va Mantiq:
721-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #721 yangi tezligi: 22 (Boshlang'ich: 16)
```


# 722-Topshiriq: Roblox Luau o'yin dasturlash asoslari #722
## Topshiriq sharti:
722-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_722 = {
    UserId = 1000 + 722,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_722:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_722:boostSpeed(7)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 722, newSpeed))
```

## Tushuntirish va Mantiq:
722-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #722 yangi tezligi: 23 (Boshlang'ich: 16)
```


# 723-Topshiriq: Roblox Luau o'yin dasturlash asoslari #723
## Topshiriq sharti:
723-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_723 = {
    UserId = 1000 + 723,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_723:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_723:boostSpeed(8)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 723, newSpeed))
```

## Tushuntirish va Mantiq:
723-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #723 yangi tezligi: 24 (Boshlang'ich: 16)
```


# 724-Topshiriq: Roblox Luau o'yin dasturlash asoslari #724
## Topshiriq sharti:
724-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_724 = {
    UserId = 1000 + 724,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_724:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_724:boostSpeed(9)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 724, newSpeed))
```

## Tushuntirish va Mantiq:
724-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #724 yangi tezligi: 25 (Boshlang'ich: 16)
```


# 725-Topshiriq: Roblox Luau o'yin dasturlash asoslari #725
## Topshiriq sharti:
725-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_725 = {
    UserId = 1000 + 725,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_725:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_725:boostSpeed(10)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 725, newSpeed))
```

## Tushuntirish va Mantiq:
725-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #725 yangi tezligi: 26 (Boshlang'ich: 16)
```


# 726-Topshiriq: Roblox Luau o'yin dasturlash asoslari #726
## Topshiriq sharti:
726-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_726 = {
    UserId = 1000 + 726,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_726:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_726:boostSpeed(11)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 726, newSpeed))
```

## Tushuntirish va Mantiq:
726-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #726 yangi tezligi: 27 (Boshlang'ich: 16)
```


# 727-Topshiriq: Roblox Luau o'yin dasturlash asoslari #727
## Topshiriq sharti:
727-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_727 = {
    UserId = 1000 + 727,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_727:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_727:boostSpeed(12)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 727, newSpeed))
```

## Tushuntirish va Mantiq:
727-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #727 yangi tezligi: 28 (Boshlang'ich: 16)
```


# 728-Topshiriq: Roblox Luau o'yin dasturlash asoslari #728
## Topshiriq sharti:
728-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_728 = {
    UserId = 1000 + 728,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_728:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_728:boostSpeed(13)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 728, newSpeed))
```

## Tushuntirish va Mantiq:
728-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #728 yangi tezligi: 29 (Boshlang'ich: 16)
```


# 729-Topshiriq: Roblox Luau o'yin dasturlash asoslari #729
## Topshiriq sharti:
729-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_729 = {
    UserId = 1000 + 729,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_729:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_729:boostSpeed(14)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 729, newSpeed))
```

## Tushuntirish va Mantiq:
729-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #729 yangi tezligi: 30 (Boshlang'ich: 16)
```


# 730-Topshiriq: Roblox Luau o'yin dasturlash asoslari #730
## Topshiriq sharti:
730-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_730 = {
    UserId = 1000 + 730,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_730:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_730:boostSpeed(5)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 730, newSpeed))
```

## Tushuntirish va Mantiq:
730-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #730 yangi tezligi: 21 (Boshlang'ich: 16)
```


# 731-Topshiriq: Roblox Luau o'yin dasturlash asoslari #731
## Topshiriq sharti:
731-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_731 = {
    UserId = 1000 + 731,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_731:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_731:boostSpeed(6)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 731, newSpeed))
```

## Tushuntirish va Mantiq:
731-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #731 yangi tezligi: 22 (Boshlang'ich: 16)
```


# 732-Topshiriq: Roblox Luau o'yin dasturlash asoslari #732
## Topshiriq sharti:
732-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_732 = {
    UserId = 1000 + 732,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_732:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_732:boostSpeed(7)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 732, newSpeed))
```

## Tushuntirish va Mantiq:
732-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #732 yangi tezligi: 23 (Boshlang'ich: 16)
```


# 733-Topshiriq: Roblox Luau o'yin dasturlash asoslari #733
## Topshiriq sharti:
733-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_733 = {
    UserId = 1000 + 733,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_733:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_733:boostSpeed(8)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 733, newSpeed))
```

## Tushuntirish va Mantiq:
733-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #733 yangi tezligi: 24 (Boshlang'ich: 16)
```


# 734-Topshiriq: Roblox Luau o'yin dasturlash asoslari #734
## Topshiriq sharti:
734-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_734 = {
    UserId = 1000 + 734,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_734:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_734:boostSpeed(9)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 734, newSpeed))
```

## Tushuntirish va Mantiq:
734-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #734 yangi tezligi: 25 (Boshlang'ich: 16)
```


# 735-Topshiriq: Roblox Luau o'yin dasturlash asoslari #735
## Topshiriq sharti:
735-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_735 = {
    UserId = 1000 + 735,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_735:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_735:boostSpeed(10)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 735, newSpeed))
```

## Tushuntirish va Mantiq:
735-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #735 yangi tezligi: 26 (Boshlang'ich: 16)
```


# 736-Topshiriq: Roblox Luau o'yin dasturlash asoslari #736
## Topshiriq sharti:
736-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_736 = {
    UserId = 1000 + 736,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_736:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_736:boostSpeed(11)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 736, newSpeed))
```

## Tushuntirish va Mantiq:
736-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #736 yangi tezligi: 27 (Boshlang'ich: 16)
```


# 737-Topshiriq: Roblox Luau o'yin dasturlash asoslari #737
## Topshiriq sharti:
737-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_737 = {
    UserId = 1000 + 737,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_737:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_737:boostSpeed(12)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 737, newSpeed))
```

## Tushuntirish va Mantiq:
737-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #737 yangi tezligi: 28 (Boshlang'ich: 16)
```


# 738-Topshiriq: Roblox Luau o'yin dasturlash asoslari #738
## Topshiriq sharti:
738-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_738 = {
    UserId = 1000 + 738,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_738:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_738:boostSpeed(13)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 738, newSpeed))
```

## Tushuntirish va Mantiq:
738-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #738 yangi tezligi: 29 (Boshlang'ich: 16)
```


# 739-Topshiriq: Roblox Luau o'yin dasturlash asoslari #739
## Topshiriq sharti:
739-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_739 = {
    UserId = 1000 + 739,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_739:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_739:boostSpeed(14)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 739, newSpeed))
```

## Tushuntirish va Mantiq:
739-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #739 yangi tezligi: 30 (Boshlang'ich: 16)
```


# 740-Topshiriq: Roblox Luau o'yin dasturlash asoslari #740
## Topshiriq sharti:
740-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_740 = {
    UserId = 1000 + 740,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_740:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_740:boostSpeed(5)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 740, newSpeed))
```

## Tushuntirish va Mantiq:
740-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #740 yangi tezligi: 21 (Boshlang'ich: 16)
```


# 741-Topshiriq: Roblox Luau o'yin dasturlash asoslari #741
## Topshiriq sharti:
741-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_741 = {
    UserId = 1000 + 741,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_741:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_741:boostSpeed(6)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 741, newSpeed))
```

## Tushuntirish va Mantiq:
741-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #741 yangi tezligi: 22 (Boshlang'ich: 16)
```


# 742-Topshiriq: Roblox Luau o'yin dasturlash asoslari #742
## Topshiriq sharti:
742-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_742 = {
    UserId = 1000 + 742,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_742:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_742:boostSpeed(7)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 742, newSpeed))
```

## Tushuntirish va Mantiq:
742-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #742 yangi tezligi: 23 (Boshlang'ich: 16)
```


# 743-Topshiriq: Roblox Luau o'yin dasturlash asoslari #743
## Topshiriq sharti:
743-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_743 = {
    UserId = 1000 + 743,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_743:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_743:boostSpeed(8)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 743, newSpeed))
```

## Tushuntirish va Mantiq:
743-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #743 yangi tezligi: 24 (Boshlang'ich: 16)
```


# 744-Topshiriq: Roblox Luau o'yin dasturlash asoslari #744
## Topshiriq sharti:
744-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_744 = {
    UserId = 1000 + 744,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_744:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_744:boostSpeed(9)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 744, newSpeed))
```

## Tushuntirish va Mantiq:
744-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #744 yangi tezligi: 25 (Boshlang'ich: 16)
```


# 745-Topshiriq: Roblox Luau o'yin dasturlash asoslari #745
## Topshiriq sharti:
745-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_745 = {
    UserId = 1000 + 745,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_745:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_745:boostSpeed(10)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 745, newSpeed))
```

## Tushuntirish va Mantiq:
745-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #745 yangi tezligi: 26 (Boshlang'ich: 16)
```


# 746-Topshiriq: Roblox Luau o'yin dasturlash asoslari #746
## Topshiriq sharti:
746-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_746 = {
    UserId = 1000 + 746,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_746:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_746:boostSpeed(11)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 746, newSpeed))
```

## Tushuntirish va Mantiq:
746-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #746 yangi tezligi: 27 (Boshlang'ich: 16)
```


# 747-Topshiriq: Roblox Luau o'yin dasturlash asoslari #747
## Topshiriq sharti:
747-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_747 = {
    UserId = 1000 + 747,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_747:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_747:boostSpeed(12)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 747, newSpeed))
```

## Tushuntirish va Mantiq:
747-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #747 yangi tezligi: 28 (Boshlang'ich: 16)
```


# 748-Topshiriq: Roblox Luau o'yin dasturlash asoslari #748
## Topshiriq sharti:
748-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_748 = {
    UserId = 1000 + 748,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_748:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_748:boostSpeed(13)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 748, newSpeed))
```

## Tushuntirish va Mantiq:
748-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #748 yangi tezligi: 29 (Boshlang'ich: 16)
```


# 749-Topshiriq: Roblox Luau o'yin dasturlash asoslari #749
## Topshiriq sharti:
749-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_749 = {
    UserId = 1000 + 749,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_749:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_749:boostSpeed(14)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 749, newSpeed))
```

## Tushuntirish va Mantiq:
749-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #749 yangi tezligi: 30 (Boshlang'ich: 16)
```


# 750-Topshiriq: Roblox Luau o'yin dasturlash asoslari #750
## Topshiriq sharti:
750-vazifa: Part xususiyatlari, o'yinchi xarakteri (Humanoid), fizika va o'yin mexanikasi.

## Yechim (Lua kodi):
```lua
local player_750 = {
    UserId = 1000 + 750,
    Health = 100,
    WalkSpeed = 16,
    JumpPower = 50
}

function player_750:boostSpeed(amount)
    self.WalkSpeed = self.WalkSpeed + amount
    return self.WalkSpeed
end

local newSpeed = player_750:boostSpeed(5)
print(string.format("O'yinchi #%d yangi tezligi: %d (Boshlang'ich: 16)", 750, newSpeed))
```

## Tushuntirish va Mantiq:
750-topshiriqda Roblox xarakterining harakat tezligi va xususiyatlarini dasturiy o'zgartirish ko'rsatildi.

## Ishlash natijasi:
```text
O'yinchi #750 yangi tezligi: 21 (Boshlang'ich: 16)
```

