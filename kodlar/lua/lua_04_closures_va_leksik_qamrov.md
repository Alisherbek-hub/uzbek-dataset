# 151-Topshiriq: Leksik qamrov (Lexical Scoping) tushunchasi
## Topshiriq sharti:
Ichki funksiya o'zining tashqi funksiyasidagi lokal o'zgaruvchiga murojaat qilishini ko'rsating.

## Yechim (Lua kodi):
```lua
local function outer()
    local secret = "MAXFIY_PAROL_2026"
    local function inner()
        print("Ichki funksiyadan o'qildi: " .. secret)
    end
    inner()
end

outer()
```

## Tushuntirish va Mantiq:
Lua leksik qamrovga ega: har bir ichki funksiya o'zi yozilgan matndagi tashqi lokal o'zgaruvchilarni ko'ra oladi.

## Ishlash natijasi:
```text
Ichki funksiyadan o'qildi: MAXFIY_PAROL_2026
```


# 152-Topshiriq: Oddiy hisoblagich (Counter Closure)
## Topshiriq sharti:
Chaqirilgan har safar o'zining ichki holatini 1 taga oshirib boruvchi closure hisoblagich yarating.

## Yechim (Lua kodi):
```lua
local function createCounter()
    local count = 0
    return function()
        count = count + 1
        return count
    end
end

local c1 = createCounter()
print("c1: " .. c1())
print("c1: " .. c1())
print("c1: " .. c1())

local c2 = createCounter()
print("c2: " .. c2())
```

## Tushuntirish va Mantiq:
Tashqi funksiya (`createCounter`) o'z ishini tugatgandan so'ng ham uning lokal 'count' o'zgaruvchisi (upvalue) xotirada saqlanib qoladi va qaytarilgan anonim funksiya tomonidan boshqariladi.

## Ishlash natijasi:
```text
c1: 1
c1: 2
c1: 3
c2: 1
```


# 153-Topshiriq: Inkapsulyatsiya va xususiy (private) ma'lumotlar
## Topshiriq sharti:
Bank hisobvarag'i balansini closure orqali to'liq tashqi aralashuvdan himoyalang.

## Yechim (Lua kodi):
```lua
local function createBankAccount(initialBalance)
    local balance = initialBalance -- Xususiy o'zgaruvchi, tashqaridan to'g'ridan-to'g'ri o'qib bo'lmaydi

    return {
        deposit = function(amount)
            if amount > 0 then
                balance = balance + amount
                print("Depozit: +" .. amount .. ", Yangi balans: " .. balance)
            end
        end,
        withdraw = function(amount)
            if amount > 0 and amount <= balance then
                balance = balance - amount
                print("Yechildi: -" .. amount .. ", Yangi balans: " .. balance)
            else
                print("Yetarli mablag' mavjud emas!")
            end
        end,
        getBalance = function()
            return balance
        end
    }
end

local account = createBankAccount(1000)
account.deposit(500)
account.withdraw(200)
print("Balans: " .. account.getBalance())
```

## Tushuntirish va Mantiq:
Luada ob'ektga xususiy (private) xususiyatlar berishning eng toza usuli bu jadval ichidagi funksiyalar va umumiy closure upvalue-laridan foydalanishdir.

## Ishlash natijasi:
```text
Depozit: +500, Yangi balans: 1500
Yechildi: -200, Yangi balans: 1300
Balans: 1300
```


# 154-Topshiriq: Memoizatsiya (Keshlovchi closure)
## Topshiriq sharti:
Og'ir matematik hisob-kitob natijalarini closure ichidagi jadvalda keshlab oluvchi funksiya yozing.

## Yechim (Lua kodi):
```lua
local function memoize(fn)
    local cache = {}
    return function(n)
        if cache[n] == nil then
            print("[HISOBLANMOQDA... " .. n .. "]")
            cache[n] = fn(n)
        else
            print("[KESHDAN OLINDI " .. n .. "]")
        end
        return cache[n]
    end
end

local slowSquare = memoize(function(x) return x * x end)
print(slowSquare(5))
print(slowSquare(5))
print(slowSquare(8))
print(slowSquare(8))
```

## Tushuntirish va Mantiq:
Memoizatsiya bir xil argumentlar bilan qayta chaqirilganda natijani keshdan darhol olib beradi va unumdorlikni oshiradi.

## Ishlash natijasi:
```text
[HISOBLANMOQDA... 5]
25
[KESHDAN OLINDI 5]
25
[HISOBLANMOQDA... 8]
64
[KESHDAN OLINDI 8]
64
```


# 155-Topshiriq: Iterator yaratish (Closure yordamida)
## Topshiriq sharti:
Massiv elementlarini ketma-ket qaytaruvchi shaxsiy iterator funksiya yasang.

## Yechim (Lua kodi):
```lua
local function arrayIterator(arr)
    local index = 0
    local count = #arr
    return function()
        index = index + 1
        if index <= count then
            return index, arr[index]
        end
    end
end

local fruits = {"Olma", "Nok", "Anor"}
local nextFruit = arrayIterator(fruits)

for idx, val in nextFruit do
    print(idx .. ": " .. val)
end
```

## Tushuntirish va Mantiq:
Luada for tsikli har bir iteratsiyada iterator funksiyani chaqiradi. Iterator nil qaytarganda for tsikli to'xtaydi.

## Ishlash natijasi:
```text
1: Olma
2: Nok
3: Anor
```


# 156-Topshiriq: Closures va leksik qamrov amaliyoti #156
## Topshiriq sharti:
156-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_156(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 156)
    end
end

local worker = makeWorker_156("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 156-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 156)
[Agent #2] Optimizatsiya (kod: 156)
```


# 157-Topshiriq: Closures va leksik qamrov amaliyoti #157
## Topshiriq sharti:
157-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_157(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 157)
    end
end

local worker = makeWorker_157("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 157-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 157)
[Agent #2] Optimizatsiya (kod: 157)
```


# 158-Topshiriq: Closures va leksik qamrov amaliyoti #158
## Topshiriq sharti:
158-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_158(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 158)
    end
end

local worker = makeWorker_158("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 158-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 158)
[Agent #2] Optimizatsiya (kod: 158)
```


# 159-Topshiriq: Closures va leksik qamrov amaliyoti #159
## Topshiriq sharti:
159-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_159(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 159)
    end
end

local worker = makeWorker_159("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 159-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 159)
[Agent #2] Optimizatsiya (kod: 159)
```


# 160-Topshiriq: Closures va leksik qamrov amaliyoti #160
## Topshiriq sharti:
160-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_160(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 160)
    end
end

local worker = makeWorker_160("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 160-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 160)
[Agent #2] Optimizatsiya (kod: 160)
```


# 161-Topshiriq: Closures va leksik qamrov amaliyoti #161
## Topshiriq sharti:
161-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_161(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 161)
    end
end

local worker = makeWorker_161("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 161-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 161)
[Agent #2] Optimizatsiya (kod: 161)
```


# 162-Topshiriq: Closures va leksik qamrov amaliyoti #162
## Topshiriq sharti:
162-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_162(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 162)
    end
end

local worker = makeWorker_162("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 162-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 162)
[Agent #2] Optimizatsiya (kod: 162)
```


# 163-Topshiriq: Closures va leksik qamrov amaliyoti #163
## Topshiriq sharti:
163-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_163(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 163)
    end
end

local worker = makeWorker_163("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 163-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 163)
[Agent #2] Optimizatsiya (kod: 163)
```


# 164-Topshiriq: Closures va leksik qamrov amaliyoti #164
## Topshiriq sharti:
164-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_164(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 164)
    end
end

local worker = makeWorker_164("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 164-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 164)
[Agent #2] Optimizatsiya (kod: 164)
```


# 165-Topshiriq: Closures va leksik qamrov amaliyoti #165
## Topshiriq sharti:
165-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_165(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 165)
    end
end

local worker = makeWorker_165("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 165-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 165)
[Agent #2] Optimizatsiya (kod: 165)
```


# 166-Topshiriq: Closures va leksik qamrov amaliyoti #166
## Topshiriq sharti:
166-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_166(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 166)
    end
end

local worker = makeWorker_166("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 166-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 166)
[Agent #2] Optimizatsiya (kod: 166)
```


# 167-Topshiriq: Closures va leksik qamrov amaliyoti #167
## Topshiriq sharti:
167-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_167(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 167)
    end
end

local worker = makeWorker_167("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 167-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 167)
[Agent #2] Optimizatsiya (kod: 167)
```


# 168-Topshiriq: Closures va leksik qamrov amaliyoti #168
## Topshiriq sharti:
168-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_168(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 168)
    end
end

local worker = makeWorker_168("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 168-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 168)
[Agent #2] Optimizatsiya (kod: 168)
```


# 169-Topshiriq: Closures va leksik qamrov amaliyoti #169
## Topshiriq sharti:
169-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_169(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 169)
    end
end

local worker = makeWorker_169("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 169-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 169)
[Agent #2] Optimizatsiya (kod: 169)
```


# 170-Topshiriq: Closures va leksik qamrov amaliyoti #170
## Topshiriq sharti:
170-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_170(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 170)
    end
end

local worker = makeWorker_170("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 170-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 170)
[Agent #2] Optimizatsiya (kod: 170)
```


# 171-Topshiriq: Closures va leksik qamrov amaliyoti #171
## Topshiriq sharti:
171-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_171(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 171)
    end
end

local worker = makeWorker_171("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 171-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 171)
[Agent #2] Optimizatsiya (kod: 171)
```


# 172-Topshiriq: Closures va leksik qamrov amaliyoti #172
## Topshiriq sharti:
172-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_172(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 172)
    end
end

local worker = makeWorker_172("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 172-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 172)
[Agent #2] Optimizatsiya (kod: 172)
```


# 173-Topshiriq: Closures va leksik qamrov amaliyoti #173
## Topshiriq sharti:
173-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_173(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 173)
    end
end

local worker = makeWorker_173("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 173-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 173)
[Agent #2] Optimizatsiya (kod: 173)
```


# 174-Topshiriq: Closures va leksik qamrov amaliyoti #174
## Topshiriq sharti:
174-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_174(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 174)
    end
end

local worker = makeWorker_174("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 174-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 174)
[Agent #2] Optimizatsiya (kod: 174)
```


# 175-Topshiriq: Closures va leksik qamrov amaliyoti #175
## Topshiriq sharti:
175-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_175(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 175)
    end
end

local worker = makeWorker_175("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 175-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 175)
[Agent #2] Optimizatsiya (kod: 175)
```


# 176-Topshiriq: Closures va leksik qamrov amaliyoti #176
## Topshiriq sharti:
176-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_176(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 176)
    end
end

local worker = makeWorker_176("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 176-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 176)
[Agent #2] Optimizatsiya (kod: 176)
```


# 177-Topshiriq: Closures va leksik qamrov amaliyoti #177
## Topshiriq sharti:
177-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_177(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 177)
    end
end

local worker = makeWorker_177("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 177-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 177)
[Agent #2] Optimizatsiya (kod: 177)
```


# 178-Topshiriq: Closures va leksik qamrov amaliyoti #178
## Topshiriq sharti:
178-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_178(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 178)
    end
end

local worker = makeWorker_178("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 178-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 178)
[Agent #2] Optimizatsiya (kod: 178)
```


# 179-Topshiriq: Closures va leksik qamrov amaliyoti #179
## Topshiriq sharti:
179-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_179(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 179)
    end
end

local worker = makeWorker_179("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 179-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 179)
[Agent #2] Optimizatsiya (kod: 179)
```


# 180-Topshiriq: Closures va leksik qamrov amaliyoti #180
## Topshiriq sharti:
180-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_180(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 180)
    end
end

local worker = makeWorker_180("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 180-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 180)
[Agent #2] Optimizatsiya (kod: 180)
```


# 181-Topshiriq: Closures va leksik qamrov amaliyoti #181
## Topshiriq sharti:
181-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_181(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 181)
    end
end

local worker = makeWorker_181("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 181-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 181)
[Agent #2] Optimizatsiya (kod: 181)
```


# 182-Topshiriq: Closures va leksik qamrov amaliyoti #182
## Topshiriq sharti:
182-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_182(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 182)
    end
end

local worker = makeWorker_182("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 182-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 182)
[Agent #2] Optimizatsiya (kod: 182)
```


# 183-Topshiriq: Closures va leksik qamrov amaliyoti #183
## Topshiriq sharti:
183-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_183(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 183)
    end
end

local worker = makeWorker_183("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 183-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 183)
[Agent #2] Optimizatsiya (kod: 183)
```


# 184-Topshiriq: Closures va leksik qamrov amaliyoti #184
## Topshiriq sharti:
184-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_184(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 184)
    end
end

local worker = makeWorker_184("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 184-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 184)
[Agent #2] Optimizatsiya (kod: 184)
```


# 185-Topshiriq: Closures va leksik qamrov amaliyoti #185
## Topshiriq sharti:
185-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_185(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 185)
    end
end

local worker = makeWorker_185("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 185-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 185)
[Agent #2] Optimizatsiya (kod: 185)
```


# 186-Topshiriq: Closures va leksik qamrov amaliyoti #186
## Topshiriq sharti:
186-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_186(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 186)
    end
end

local worker = makeWorker_186("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 186-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 186)
[Agent #2] Optimizatsiya (kod: 186)
```


# 187-Topshiriq: Closures va leksik qamrov amaliyoti #187
## Topshiriq sharti:
187-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_187(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 187)
    end
end

local worker = makeWorker_187("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 187-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 187)
[Agent #2] Optimizatsiya (kod: 187)
```


# 188-Topshiriq: Closures va leksik qamrov amaliyoti #188
## Topshiriq sharti:
188-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_188(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 188)
    end
end

local worker = makeWorker_188("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 188-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 188)
[Agent #2] Optimizatsiya (kod: 188)
```


# 189-Topshiriq: Closures va leksik qamrov amaliyoti #189
## Topshiriq sharti:
189-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_189(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 189)
    end
end

local worker = makeWorker_189("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 189-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 189)
[Agent #2] Optimizatsiya (kod: 189)
```


# 190-Topshiriq: Closures va leksik qamrov amaliyoti #190
## Topshiriq sharti:
190-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_190(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 190)
    end
end

local worker = makeWorker_190("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 190-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 190)
[Agent #2] Optimizatsiya (kod: 190)
```


# 191-Topshiriq: Closures va leksik qamrov amaliyoti #191
## Topshiriq sharti:
191-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_191(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 191)
    end
end

local worker = makeWorker_191("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 191-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 191)
[Agent #2] Optimizatsiya (kod: 191)
```


# 192-Topshiriq: Closures va leksik qamrov amaliyoti #192
## Topshiriq sharti:
192-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_192(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 192)
    end
end

local worker = makeWorker_192("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 192-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 192)
[Agent #2] Optimizatsiya (kod: 192)
```


# 193-Topshiriq: Closures va leksik qamrov amaliyoti #193
## Topshiriq sharti:
193-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_193(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 193)
    end
end

local worker = makeWorker_193("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 193-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 193)
[Agent #2] Optimizatsiya (kod: 193)
```


# 194-Topshiriq: Closures va leksik qamrov amaliyoti #194
## Topshiriq sharti:
194-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_194(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 194)
    end
end

local worker = makeWorker_194("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 194-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 194)
[Agent #2] Optimizatsiya (kod: 194)
```


# 195-Topshiriq: Closures va leksik qamrov amaliyoti #195
## Topshiriq sharti:
195-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_195(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 195)
    end
end

local worker = makeWorker_195("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 195-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 195)
[Agent #2] Optimizatsiya (kod: 195)
```


# 196-Topshiriq: Closures va leksik qamrov amaliyoti #196
## Topshiriq sharti:
196-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_196(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 196)
    end
end

local worker = makeWorker_196("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 196-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 196)
[Agent #2] Optimizatsiya (kod: 196)
```


# 197-Topshiriq: Closures va leksik qamrov amaliyoti #197
## Topshiriq sharti:
197-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_197(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 197)
    end
end

local worker = makeWorker_197("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 197-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 197)
[Agent #2] Optimizatsiya (kod: 197)
```


# 198-Topshiriq: Closures va leksik qamrov amaliyoti #198
## Topshiriq sharti:
198-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_198(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 198)
    end
end

local worker = makeWorker_198("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 198-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 198)
[Agent #2] Optimizatsiya (kod: 198)
```


# 199-Topshiriq: Closures va leksik qamrov amaliyoti #199
## Topshiriq sharti:
199-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_199(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 199)
    end
end

local worker = makeWorker_199("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 199-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 199)
[Agent #2] Optimizatsiya (kod: 199)
```


# 200-Topshiriq: Closures va leksik qamrov amaliyoti #200
## Topshiriq sharti:
200-vazifa: Upvalues, holat saqlovchi yopiq muhitlar (closures) va funksional factory yechimini namoyish qiling.

## Yechim (Lua kodi):
```lua
local function makeWorker_200(prefix)
    local jobCount = 0
    return function(taskName)
        jobCount = jobCount + 1
        return string.format("[%s #%d] %s (kod: %d)", prefix, jobCount, taskName, 200)
    end
end

local worker = makeWorker_200("Agent")
print(worker("Diagnostika"))
print(worker("Optimizatsiya"))
```

## Tushuntirish va Mantiq:
Ushbu 200-topshiriqda closure yordamida prefix va jobCount upvaluelari saqlanib, holat monitoringi ta'minlandi.

## Ishlash natijasi:
```text
[Agent #1] Diagnostika (kod: 200)
[Agent #2] Optimizatsiya (kod: 200)
```

