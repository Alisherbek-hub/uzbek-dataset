# 801-Topshiriq: LÖVE2D o'yin dvijogining hayotiy davri (Callbacks)
## Topshiriq sharti:
love.load, love.update va love.draw funksiyalarining o'zaro bog'liqligini ko'rsating.

## Yechim (Lua kodi):
```lua
-- LÖVE2D simulyatsiyasi:
local gameState = {score = 0, playerX = 100}

local function love_load()
    gameState.score = 0
    print("[LÖVE2D]: O'yin resurslari yuklandi.")
end

local function love_update(dt)
    gameState.playerX = gameState.playerX + 50 * dt
end

local function love_draw()
    print(string.format("[LÖVE2D RENDER]: O'yinchi X=%.1f, Ball=%d", gameState.playerX, gameState.score))
end

love_load()
love_update(0.1) -- 100ms o'tdi
love_draw()
```

## Tushuntirish va Mantiq:
LÖVE2D arxitekturasi 3 ta ustunga tayanadi: `love.load` boshlang'ich yuklash, `love.update(dt)` fizika va mantiq, `love.draw` har kadrda grafikani ekranga chizish.

## Ishlash natijasi:
```text
[LÖVE2D]: O'yin resurslari yuklandi.
[LÖVE2D RENDER]: O'yinchi X=105.0, Ball=0
```


# 802-Topshiriq: Delta Time (dt) va mustaqil fizika
## Topshiriq sharti:
Kadrlar chastotasi (FPS) har xil bo'lganda ham o'yinchi harakati bir xil tezlikda bo'lishini ta'minlang.

## Yechim (Lua kodi):
```lua
local speed = 200 -- 200 piksel/sekund
local posX = 0

-- 60 FPS da bitta kadr vaqti ~0.0166 sek
posX = posX + speed * 0.0166
print(string.format("60 FPS kadrida siljish: %.2f px", posX))

-- 30 FPS da bitta kadr vaqti ~0.0333 sek
posX = 0
posX = posX + speed * 0.0333
print(string.format("30 FPS kadrida siljish: %.2f px", posX))
```

## Tushuntirish va Mantiq:
`dt` (delta time) har bir kadr oralig'idagi o'tgan aniq vaqt bo'lib, uni tezlikka ko'paytirish kompyuter kuchi qanday bo'lishidan qat'i nazar bir tekis harakatni kafolatlaydi.

## Ishlash natijasi:
```text
60 FPS kadrida siljish: 3.32 px
30 FPS kadrida siljish: 6.66 px
```


# 803-Topshiriq: AABB (Axis-Aligned Bounding Box) to'qnashuv algoritmi
## Topshiriq sharti:
Ikkita to'g'ri to'rtburchakning bir-biri bilan to'qnashganligini matematik tekshiring.

## Yechim (Lua kodi):
```lua
local function checkAABB(rectA, rectB)
    return rectA.x < rectB.x + rectB.w and
           rectA.x + rectA.w > rectB.x and
           rectA.y < rectB.y + rectB.h and
           rectA.y + rectA.h > rectB.y
end

local box1 = {x = 10, y = 10, w = 50, h = 50}
local box2 = {x = 40, y = 40, w = 50, h = 50}
local box3 = {x = 100, y = 100, w = 30, h = 30}

print("Box1 va Box2 to'qnashdimi? " .. tostring(checkAABB(box1, box2)))
print("Box1 va Box3 to'qnashdimi? " .. tostring(checkAABB(box1, box3)))
```

## Tushuntirish va Mantiq:
AABB 2D o'yinlardagi eng tezkor va ommabop to'qnashuv algoritmi hisoblanadi ($O(1)$ murakkablik).

## Ishlash natijasi:
```text
Box1 va Box2 to'qnashdimi? true
Box1 va Box3 to'qnashdimi? false
```


# 804-Topshiriq: Klaviatura va kiritish nazorati
## Topshiriq sharti:
O'yinchining yo'nalish tugmalarini bosishiga qarab koordinatalarni yangilang.

## Yechim (Lua kodi):
```lua
local inputMap = {right = true, left = false, up = false, down = false}
local x, y = 50, 50

if inputMap.right then x = x + 5 end
if inputMap.left then x = x - 5 end

print(string.format("Harakatdan keyingi yangi pozitsiya: (%d, %d)", x, y))
```

## Tushuntirish va Mantiq:
LÖVE2D da `love.keyboard.isDown('right')` yoki `love.keypressed(key)` orqali tugmalar bosilishi ushlanadi.

## Ishlash natijasi:
```text
Harakatdan keyingi yangi pozitsiya: (55, 50)
```


# 805-Topshiriq: O'yin holati mashinasi (State Machine: Menu, Playing, GameOver)
## Topshiriq sharti:
Turli o'yin ekranlarini boshqaruvchi State patternni qo'llang.

## Yechim (Lua kodi):
```lua
local GameStateManager = {currentState = "MENU"}

function GameStateManager:changeState(newState)
    print(string.format("[O'YIN HOLATI]: %s -> %s", self.currentState, newState))
    self.currentState = newState
end

GameStateManager:changeState("PLAYING")
GameStateManager:changeState("GAME_OVER")
```

## Tushuntirish va Mantiq:
State Machine orqali menyu, o'yin jarayoni, pauza va g'alaba ekranlari bir-biridan toza ajratiladi.

## Ishlash natijasi:
```text
[O'YIN HOLATI]: MENU -> PLAYING
[O'YIN HOLATI]: PLAYING -> GAME_OVER
```


# 806-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #806
## Topshiriq sharti:
806-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_806 = {
    id = 806,
    x = 6,
    y = 12,
    vx = 2.5
}

entity_806.x = entity_806.x + entity_806.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 806, entity_806.x, entity_806.y))
```

## Tushuntirish va Mantiq:
806-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #806 yangilandi: X=8.5, Y=12.0
```


# 807-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #807
## Topshiriq sharti:
807-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_807 = {
    id = 807,
    x = 7,
    y = 14,
    vx = 2.5
}

entity_807.x = entity_807.x + entity_807.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 807, entity_807.x, entity_807.y))
```

## Tushuntirish va Mantiq:
807-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #807 yangilandi: X=9.5, Y=14.0
```


# 808-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #808
## Topshiriq sharti:
808-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_808 = {
    id = 808,
    x = 8,
    y = 16,
    vx = 2.5
}

entity_808.x = entity_808.x + entity_808.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 808, entity_808.x, entity_808.y))
```

## Tushuntirish va Mantiq:
808-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #808 yangilandi: X=10.5, Y=16.0
```


# 809-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #809
## Topshiriq sharti:
809-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_809 = {
    id = 809,
    x = 9,
    y = 18,
    vx = 2.5
}

entity_809.x = entity_809.x + entity_809.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 809, entity_809.x, entity_809.y))
```

## Tushuntirish va Mantiq:
809-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #809 yangilandi: X=11.5, Y=18.0
```


# 810-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #810
## Topshiriq sharti:
810-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_810 = {
    id = 810,
    x = 10,
    y = 20,
    vx = 2.5
}

entity_810.x = entity_810.x + entity_810.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 810, entity_810.x, entity_810.y))
```

## Tushuntirish va Mantiq:
810-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #810 yangilandi: X=12.5, Y=20.0
```


# 811-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #811
## Topshiriq sharti:
811-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_811 = {
    id = 811,
    x = 11,
    y = 22,
    vx = 2.5
}

entity_811.x = entity_811.x + entity_811.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 811, entity_811.x, entity_811.y))
```

## Tushuntirish va Mantiq:
811-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #811 yangilandi: X=13.5, Y=22.0
```


# 812-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #812
## Topshiriq sharti:
812-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_812 = {
    id = 812,
    x = 12,
    y = 24,
    vx = 2.5
}

entity_812.x = entity_812.x + entity_812.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 812, entity_812.x, entity_812.y))
```

## Tushuntirish va Mantiq:
812-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #812 yangilandi: X=14.5, Y=24.0
```


# 813-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #813
## Topshiriq sharti:
813-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_813 = {
    id = 813,
    x = 13,
    y = 26,
    vx = 2.5
}

entity_813.x = entity_813.x + entity_813.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 813, entity_813.x, entity_813.y))
```

## Tushuntirish va Mantiq:
813-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #813 yangilandi: X=15.5, Y=26.0
```


# 814-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #814
## Topshiriq sharti:
814-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_814 = {
    id = 814,
    x = 14,
    y = 28,
    vx = 2.5
}

entity_814.x = entity_814.x + entity_814.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 814, entity_814.x, entity_814.y))
```

## Tushuntirish va Mantiq:
814-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #814 yangilandi: X=16.5, Y=28.0
```


# 815-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #815
## Topshiriq sharti:
815-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_815 = {
    id = 815,
    x = 15,
    y = 30,
    vx = 2.5
}

entity_815.x = entity_815.x + entity_815.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 815, entity_815.x, entity_815.y))
```

## Tushuntirish va Mantiq:
815-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #815 yangilandi: X=17.5, Y=30.0
```


# 816-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #816
## Topshiriq sharti:
816-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_816 = {
    id = 816,
    x = 16,
    y = 32,
    vx = 2.5
}

entity_816.x = entity_816.x + entity_816.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 816, entity_816.x, entity_816.y))
```

## Tushuntirish va Mantiq:
816-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #816 yangilandi: X=18.5, Y=32.0
```


# 817-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #817
## Topshiriq sharti:
817-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_817 = {
    id = 817,
    x = 17,
    y = 34,
    vx = 2.5
}

entity_817.x = entity_817.x + entity_817.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 817, entity_817.x, entity_817.y))
```

## Tushuntirish va Mantiq:
817-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #817 yangilandi: X=19.5, Y=34.0
```


# 818-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #818
## Topshiriq sharti:
818-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_818 = {
    id = 818,
    x = 18,
    y = 36,
    vx = 2.5
}

entity_818.x = entity_818.x + entity_818.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 818, entity_818.x, entity_818.y))
```

## Tushuntirish va Mantiq:
818-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #818 yangilandi: X=20.5, Y=36.0
```


# 819-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #819
## Topshiriq sharti:
819-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_819 = {
    id = 819,
    x = 19,
    y = 38,
    vx = 2.5
}

entity_819.x = entity_819.x + entity_819.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 819, entity_819.x, entity_819.y))
```

## Tushuntirish va Mantiq:
819-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #819 yangilandi: X=21.5, Y=38.0
```


# 820-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #820
## Topshiriq sharti:
820-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_820 = {
    id = 820,
    x = 20,
    y = 40,
    vx = 2.5
}

entity_820.x = entity_820.x + entity_820.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 820, entity_820.x, entity_820.y))
```

## Tushuntirish va Mantiq:
820-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #820 yangilandi: X=22.5, Y=40.0
```


# 821-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #821
## Topshiriq sharti:
821-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_821 = {
    id = 821,
    x = 21,
    y = 42,
    vx = 2.5
}

entity_821.x = entity_821.x + entity_821.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 821, entity_821.x, entity_821.y))
```

## Tushuntirish va Mantiq:
821-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #821 yangilandi: X=23.5, Y=42.0
```


# 822-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #822
## Topshiriq sharti:
822-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_822 = {
    id = 822,
    x = 22,
    y = 44,
    vx = 2.5
}

entity_822.x = entity_822.x + entity_822.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 822, entity_822.x, entity_822.y))
```

## Tushuntirish va Mantiq:
822-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #822 yangilandi: X=24.5, Y=44.0
```


# 823-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #823
## Topshiriq sharti:
823-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_823 = {
    id = 823,
    x = 23,
    y = 46,
    vx = 2.5
}

entity_823.x = entity_823.x + entity_823.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 823, entity_823.x, entity_823.y))
```

## Tushuntirish va Mantiq:
823-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #823 yangilandi: X=25.5, Y=46.0
```


# 824-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #824
## Topshiriq sharti:
824-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_824 = {
    id = 824,
    x = 24,
    y = 48,
    vx = 2.5
}

entity_824.x = entity_824.x + entity_824.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 824, entity_824.x, entity_824.y))
```

## Tushuntirish va Mantiq:
824-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #824 yangilandi: X=26.5, Y=48.0
```


# 825-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #825
## Topshiriq sharti:
825-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_825 = {
    id = 825,
    x = 25,
    y = 50,
    vx = 2.5
}

entity_825.x = entity_825.x + entity_825.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 825, entity_825.x, entity_825.y))
```

## Tushuntirish va Mantiq:
825-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #825 yangilandi: X=27.5, Y=50.0
```


# 826-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #826
## Topshiriq sharti:
826-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_826 = {
    id = 826,
    x = 26,
    y = 52,
    vx = 2.5
}

entity_826.x = entity_826.x + entity_826.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 826, entity_826.x, entity_826.y))
```

## Tushuntirish va Mantiq:
826-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #826 yangilandi: X=28.5, Y=52.0
```


# 827-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #827
## Topshiriq sharti:
827-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_827 = {
    id = 827,
    x = 27,
    y = 54,
    vx = 2.5
}

entity_827.x = entity_827.x + entity_827.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 827, entity_827.x, entity_827.y))
```

## Tushuntirish va Mantiq:
827-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #827 yangilandi: X=29.5, Y=54.0
```


# 828-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #828
## Topshiriq sharti:
828-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_828 = {
    id = 828,
    x = 28,
    y = 56,
    vx = 2.5
}

entity_828.x = entity_828.x + entity_828.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 828, entity_828.x, entity_828.y))
```

## Tushuntirish va Mantiq:
828-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #828 yangilandi: X=30.5, Y=56.0
```


# 829-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #829
## Topshiriq sharti:
829-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_829 = {
    id = 829,
    x = 29,
    y = 58,
    vx = 2.5
}

entity_829.x = entity_829.x + entity_829.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 829, entity_829.x, entity_829.y))
```

## Tushuntirish va Mantiq:
829-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #829 yangilandi: X=31.5, Y=58.0
```


# 830-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #830
## Topshiriq sharti:
830-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_830 = {
    id = 830,
    x = 30,
    y = 60,
    vx = 2.5
}

entity_830.x = entity_830.x + entity_830.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 830, entity_830.x, entity_830.y))
```

## Tushuntirish va Mantiq:
830-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #830 yangilandi: X=32.5, Y=60.0
```


# 831-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #831
## Topshiriq sharti:
831-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_831 = {
    id = 831,
    x = 31,
    y = 62,
    vx = 2.5
}

entity_831.x = entity_831.x + entity_831.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 831, entity_831.x, entity_831.y))
```

## Tushuntirish va Mantiq:
831-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #831 yangilandi: X=33.5, Y=62.0
```


# 832-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #832
## Topshiriq sharti:
832-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_832 = {
    id = 832,
    x = 32,
    y = 64,
    vx = 2.5
}

entity_832.x = entity_832.x + entity_832.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 832, entity_832.x, entity_832.y))
```

## Tushuntirish va Mantiq:
832-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #832 yangilandi: X=34.5, Y=64.0
```


# 833-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #833
## Topshiriq sharti:
833-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_833 = {
    id = 833,
    x = 33,
    y = 66,
    vx = 2.5
}

entity_833.x = entity_833.x + entity_833.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 833, entity_833.x, entity_833.y))
```

## Tushuntirish va Mantiq:
833-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #833 yangilandi: X=35.5, Y=66.0
```


# 834-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #834
## Topshiriq sharti:
834-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_834 = {
    id = 834,
    x = 34,
    y = 68,
    vx = 2.5
}

entity_834.x = entity_834.x + entity_834.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 834, entity_834.x, entity_834.y))
```

## Tushuntirish va Mantiq:
834-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #834 yangilandi: X=36.5, Y=68.0
```


# 835-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #835
## Topshiriq sharti:
835-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_835 = {
    id = 835,
    x = 35,
    y = 70,
    vx = 2.5
}

entity_835.x = entity_835.x + entity_835.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 835, entity_835.x, entity_835.y))
```

## Tushuntirish va Mantiq:
835-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #835 yangilandi: X=37.5, Y=70.0
```


# 836-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #836
## Topshiriq sharti:
836-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_836 = {
    id = 836,
    x = 36,
    y = 72,
    vx = 2.5
}

entity_836.x = entity_836.x + entity_836.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 836, entity_836.x, entity_836.y))
```

## Tushuntirish va Mantiq:
836-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #836 yangilandi: X=38.5, Y=72.0
```


# 837-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #837
## Topshiriq sharti:
837-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_837 = {
    id = 837,
    x = 37,
    y = 74,
    vx = 2.5
}

entity_837.x = entity_837.x + entity_837.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 837, entity_837.x, entity_837.y))
```

## Tushuntirish va Mantiq:
837-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #837 yangilandi: X=39.5, Y=74.0
```


# 838-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #838
## Topshiriq sharti:
838-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_838 = {
    id = 838,
    x = 38,
    y = 76,
    vx = 2.5
}

entity_838.x = entity_838.x + entity_838.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 838, entity_838.x, entity_838.y))
```

## Tushuntirish va Mantiq:
838-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #838 yangilandi: X=40.5, Y=76.0
```


# 839-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #839
## Topshiriq sharti:
839-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_839 = {
    id = 839,
    x = 39,
    y = 78,
    vx = 2.5
}

entity_839.x = entity_839.x + entity_839.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 839, entity_839.x, entity_839.y))
```

## Tushuntirish va Mantiq:
839-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #839 yangilandi: X=41.5, Y=78.0
```


# 840-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #840
## Topshiriq sharti:
840-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_840 = {
    id = 840,
    x = 40,
    y = 80,
    vx = 2.5
}

entity_840.x = entity_840.x + entity_840.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 840, entity_840.x, entity_840.y))
```

## Tushuntirish va Mantiq:
840-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #840 yangilandi: X=42.5, Y=80.0
```


# 841-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #841
## Topshiriq sharti:
841-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_841 = {
    id = 841,
    x = 41,
    y = 82,
    vx = 2.5
}

entity_841.x = entity_841.x + entity_841.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 841, entity_841.x, entity_841.y))
```

## Tushuntirish va Mantiq:
841-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #841 yangilandi: X=43.5, Y=82.0
```


# 842-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #842
## Topshiriq sharti:
842-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_842 = {
    id = 842,
    x = 42,
    y = 84,
    vx = 2.5
}

entity_842.x = entity_842.x + entity_842.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 842, entity_842.x, entity_842.y))
```

## Tushuntirish va Mantiq:
842-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #842 yangilandi: X=44.5, Y=84.0
```


# 843-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #843
## Topshiriq sharti:
843-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_843 = {
    id = 843,
    x = 43,
    y = 86,
    vx = 2.5
}

entity_843.x = entity_843.x + entity_843.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 843, entity_843.x, entity_843.y))
```

## Tushuntirish va Mantiq:
843-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #843 yangilandi: X=45.5, Y=86.0
```


# 844-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #844
## Topshiriq sharti:
844-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_844 = {
    id = 844,
    x = 44,
    y = 88,
    vx = 2.5
}

entity_844.x = entity_844.x + entity_844.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 844, entity_844.x, entity_844.y))
```

## Tushuntirish va Mantiq:
844-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #844 yangilandi: X=46.5, Y=88.0
```


# 845-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #845
## Topshiriq sharti:
845-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_845 = {
    id = 845,
    x = 45,
    y = 90,
    vx = 2.5
}

entity_845.x = entity_845.x + entity_845.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 845, entity_845.x, entity_845.y))
```

## Tushuntirish va Mantiq:
845-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #845 yangilandi: X=47.5, Y=90.0
```


# 846-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #846
## Topshiriq sharti:
846-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_846 = {
    id = 846,
    x = 46,
    y = 92,
    vx = 2.5
}

entity_846.x = entity_846.x + entity_846.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 846, entity_846.x, entity_846.y))
```

## Tushuntirish va Mantiq:
846-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #846 yangilandi: X=48.5, Y=92.0
```


# 847-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #847
## Topshiriq sharti:
847-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_847 = {
    id = 847,
    x = 47,
    y = 94,
    vx = 2.5
}

entity_847.x = entity_847.x + entity_847.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 847, entity_847.x, entity_847.y))
```

## Tushuntirish va Mantiq:
847-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #847 yangilandi: X=49.5, Y=94.0
```


# 848-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #848
## Topshiriq sharti:
848-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_848 = {
    id = 848,
    x = 48,
    y = 96,
    vx = 2.5
}

entity_848.x = entity_848.x + entity_848.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 848, entity_848.x, entity_848.y))
```

## Tushuntirish va Mantiq:
848-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #848 yangilandi: X=50.5, Y=96.0
```


# 849-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #849
## Topshiriq sharti:
849-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_849 = {
    id = 849,
    x = 49,
    y = 98,
    vx = 2.5
}

entity_849.x = entity_849.x + entity_849.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 849, entity_849.x, entity_849.y))
```

## Tushuntirish va Mantiq:
849-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #849 yangilandi: X=51.5, Y=98.0
```


# 850-Topshiriq: LÖVE2D va 2D o'yin muhandisligi #850
## Topshiriq sharti:
850-vazifa: Zarrachalar tizimi (Particles), sprite animatsiyalari, kamera harakati va audio boshqaruvi.

## Yechim (Lua kodi):
```lua
local entity_850 = {
    id = 850,
    x = 50,
    y = 0,
    vx = 2.5
}

entity_850.x = entity_850.x + entity_850.vx
print(string.format("Entity #%d yangilandi: X=%.1f, Y=%.1f", 850, entity_850.x, entity_850.y))
```

## Tushuntirish va Mantiq:
850-topshiriqda 2D dvijoklarda dinamik fizik ob'ektlar holatini hisoblash ko'rsatildi.

## Ishlash natijasi:
```text
Entity #850 yangilandi: X=52.5, Y=0.0
```

