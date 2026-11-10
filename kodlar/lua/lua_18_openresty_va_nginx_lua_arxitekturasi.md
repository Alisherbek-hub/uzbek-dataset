# 851-Topshiriq: OpenResty arxitekturasi va content_by_lua_block
## Topshiriq sharti:
Nginx ichida to'g'ridan-to'g'ri Lua orqali HTTP javob qaytarish mantig'ini ko'rsating.

## Yechim (Lua kodi):
```lua
-- Nginx OpenResty simulyatsiyasi:
local ngx_mock = {
    say = function(msg) print("[NGINX RESPONSE]: " .. msg) end,
    status = 200
}

ngx_mock.status = 200
ngx_mock.say("Salom! Ushbu javob OpenResty LuaJIT tomonidan berildi.")
```

## Tushuntirish va Mantiq:
OpenResty Nginx veb-serveri ichida LuaJIT ni ishlatib, sekundiga yuz minglab so'rovlarni nosintezator asinxron rejimda qayta ishlaydi.

## Ishlash natijasi:
```text
[NGINX RESPONSE]: Salom! Ushbu javob OpenResty LuaJIT tomonidan berildi.
```


# 852-Topshiriq: HTTP so'rov parametrlarini o'qish: ngx.req.get_uri_args
## Topshiriq sharti:
URL query parametrlarini (?user=ali&page=2) ajratib oluvchi skript yozing.

## Yechim (Lua kodi):
```lua
local mockQueryArgs = {user = "bobur", page = "3"}

print("Foydalanuvchi parametri: " .. mockQueryArgs.user)
print("Sahifa: " .. mockQueryArgs.page)
```

## Tushuntirish va Mantiq:
`ngx.req.get_uri_args()` barcha GET parametrlarini Lua jadvaliga xesh-xarita ko'rinishida o'girib beradi.

## Ishlash natijasi:
```text
Foydalanuvchi parametri: bobur
Sahifa: 3
```


# 853-Topshiriq: access_by_lua_block orqali API Gateway Autentifikatsiyasi
## Topshiriq sharti:
So'rov bosh sarlavhasida (Headers) Authorization tokenini tekshirib ruxsat beruvchi xavfsizlik qatlami.

## Yechim (Lua kodi):
```lua
local headers = {["Authorization"] = "Bearer SECRET_API_KEY_2026"}

local function checkAccess(reqHeaders)
    local auth = reqHeaders["Authorization"]
    if auth == "Bearer SECRET_API_KEY_2026" then
        print("[ACCESS GRANTED]: Ruxsat berildi.")
        return true
    else
        print("[ACCESS DENIED]: 401 Unauthorized.")
        return false
    end
end

checkAccess(headers)
```

## Tushuntirish va Mantiq:
`access_by_lua` bosqichida Nginx so'rovni asosiy backendga (Upstream) yuborishdan oldin tekshiradi, bu backend yukini keskin kamaytiradi.

## Ishlash natijasi:
```text
[ACCESS GRANTED]: Ruxsat berildi.
```


# 854-Topshiriq: lua_shared_dict orqali umumiy kesh xotirasi
## Topshiriq sharti:
Barcha Nginx worker jarayonlari o'rtasida umumiy bo'lgan tezkor RAM lug'atidan foydalanish.

## Yechim (Lua kodi):
```lua
local sharedDict = {}

local function cacheSet(key, val) sharedDict[key] = val end
local function cacheGet(key) return sharedDict[key] end

cacheSet("user:101", "Alisher Navoiy")
print("Keshdan o'qildi: " .. cacheGet("user:101"))
```

## Tushuntirish va Mantiq:
`lua_shared_dict` Nginx workerlari o'rtasida umumiy xotirani ta'minlaydi va Redis yoki DB ga murojaatsiz mikrosekundlarda javob qaytarish imkonini beradi.

## Ishlash natijasi:
```text
Keshdan o'qildi: Alisher Navoiy
```


# 855-Topshiriq: Rate Limiter (So'rovlar chastotasini cheklash)
## Topshiriq sharti:
Bitta IP manzildan belgilangan miqdordan ortiq so'rov kelsa 429 xatosini beruvchi cheklovchi tuzing.

## Yechim (Lua kodi):
```lua
local requestsPerIP = {["192.168.1.50"] = 10}
local LIMIT = 10

local function checkRateLimit(ip)
    local count = requestsPerIP[ip] or 0
    if count >= LIMIT then
        print(string.format("[RATE LIMIT 429]: IP %s chegaraga yetdi!", ip))
        return false
    end
    requestsPerIP[ip] = count + 1
    return true
end

checkRateLimit("192.168.1.50")
```

## Tushuntirish va Mantiq:
OpenResty Rate Limiter API larni DDoS va ortiqcha yuklamalardan himoya qilishda standart sanoat yechimidir (masalan, Cloudflare da).

## Ishlash natijasi:
```text
[RATE LIMIT 429]: IP 192.168.1.50 chegaraga yetdi!
```


# 856-Topshiriq: OpenResty va Nginx Lua arxitekturasi #856
## Topshiriq sharti:
856-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_856 = {
    host = "10.0.1.106",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    856, upstreamNode_856.host, upstreamNode_856.port, upstreamNode_856.weight))
```

## Tushuntirish va Mantiq:
856-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #856: http://10.0.1.106:8080 (Og'irlik: 2)
```


# 857-Topshiriq: OpenResty va Nginx Lua arxitekturasi #857
## Topshiriq sharti:
857-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_857 = {
    host = "10.0.1.107",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    857, upstreamNode_857.host, upstreamNode_857.port, upstreamNode_857.weight))
```

## Tushuntirish va Mantiq:
857-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #857: http://10.0.1.107:8080 (Og'irlik: 3)
```


# 858-Topshiriq: OpenResty va Nginx Lua arxitekturasi #858
## Topshiriq sharti:
858-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_858 = {
    host = "10.0.1.108",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    858, upstreamNode_858.host, upstreamNode_858.port, upstreamNode_858.weight))
```

## Tushuntirish va Mantiq:
858-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #858: http://10.0.1.108:8080 (Og'irlik: 4)
```


# 859-Topshiriq: OpenResty va Nginx Lua arxitekturasi #859
## Topshiriq sharti:
859-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_859 = {
    host = "10.0.1.109",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    859, upstreamNode_859.host, upstreamNode_859.port, upstreamNode_859.weight))
```

## Tushuntirish va Mantiq:
859-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #859: http://10.0.1.109:8080 (Og'irlik: 5)
```


# 860-Topshiriq: OpenResty va Nginx Lua arxitekturasi #860
## Topshiriq sharti:
860-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_860 = {
    host = "10.0.1.110",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    860, upstreamNode_860.host, upstreamNode_860.port, upstreamNode_860.weight))
```

## Tushuntirish va Mantiq:
860-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #860: http://10.0.1.110:8080 (Og'irlik: 1)
```


# 861-Topshiriq: OpenResty va Nginx Lua arxitekturasi #861
## Topshiriq sharti:
861-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_861 = {
    host = "10.0.1.111",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    861, upstreamNode_861.host, upstreamNode_861.port, upstreamNode_861.weight))
```

## Tushuntirish va Mantiq:
861-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #861: http://10.0.1.111:8080 (Og'irlik: 2)
```


# 862-Topshiriq: OpenResty va Nginx Lua arxitekturasi #862
## Topshiriq sharti:
862-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_862 = {
    host = "10.0.1.112",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    862, upstreamNode_862.host, upstreamNode_862.port, upstreamNode_862.weight))
```

## Tushuntirish va Mantiq:
862-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #862: http://10.0.1.112:8080 (Og'irlik: 3)
```


# 863-Topshiriq: OpenResty va Nginx Lua arxitekturasi #863
## Topshiriq sharti:
863-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_863 = {
    host = "10.0.1.113",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    863, upstreamNode_863.host, upstreamNode_863.port, upstreamNode_863.weight))
```

## Tushuntirish va Mantiq:
863-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #863: http://10.0.1.113:8080 (Og'irlik: 4)
```


# 864-Topshiriq: OpenResty va Nginx Lua arxitekturasi #864
## Topshiriq sharti:
864-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_864 = {
    host = "10.0.1.114",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    864, upstreamNode_864.host, upstreamNode_864.port, upstreamNode_864.weight))
```

## Tushuntirish va Mantiq:
864-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #864: http://10.0.1.114:8080 (Og'irlik: 5)
```


# 865-Topshiriq: OpenResty va Nginx Lua arxitekturasi #865
## Topshiriq sharti:
865-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_865 = {
    host = "10.0.1.115",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    865, upstreamNode_865.host, upstreamNode_865.port, upstreamNode_865.weight))
```

## Tushuntirish va Mantiq:
865-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #865: http://10.0.1.115:8080 (Og'irlik: 1)
```


# 866-Topshiriq: OpenResty va Nginx Lua arxitekturasi #866
## Topshiriq sharti:
866-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_866 = {
    host = "10.0.1.116",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    866, upstreamNode_866.host, upstreamNode_866.port, upstreamNode_866.weight))
```

## Tushuntirish va Mantiq:
866-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #866: http://10.0.1.116:8080 (Og'irlik: 2)
```


# 867-Topshiriq: OpenResty va Nginx Lua arxitekturasi #867
## Topshiriq sharti:
867-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_867 = {
    host = "10.0.1.117",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    867, upstreamNode_867.host, upstreamNode_867.port, upstreamNode_867.weight))
```

## Tushuntirish va Mantiq:
867-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #867: http://10.0.1.117:8080 (Og'irlik: 3)
```


# 868-Topshiriq: OpenResty va Nginx Lua arxitekturasi #868
## Topshiriq sharti:
868-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_868 = {
    host = "10.0.1.118",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    868, upstreamNode_868.host, upstreamNode_868.port, upstreamNode_868.weight))
```

## Tushuntirish va Mantiq:
868-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #868: http://10.0.1.118:8080 (Og'irlik: 4)
```


# 869-Topshiriq: OpenResty va Nginx Lua arxitekturasi #869
## Topshiriq sharti:
869-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_869 = {
    host = "10.0.1.119",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    869, upstreamNode_869.host, upstreamNode_869.port, upstreamNode_869.weight))
```

## Tushuntirish va Mantiq:
869-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #869: http://10.0.1.119:8080 (Og'irlik: 5)
```


# 870-Topshiriq: OpenResty va Nginx Lua arxitekturasi #870
## Topshiriq sharti:
870-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_870 = {
    host = "10.0.1.120",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    870, upstreamNode_870.host, upstreamNode_870.port, upstreamNode_870.weight))
```

## Tushuntirish va Mantiq:
870-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #870: http://10.0.1.120:8080 (Og'irlik: 1)
```


# 871-Topshiriq: OpenResty va Nginx Lua arxitekturasi #871
## Topshiriq sharti:
871-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_871 = {
    host = "10.0.1.121",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    871, upstreamNode_871.host, upstreamNode_871.port, upstreamNode_871.weight))
```

## Tushuntirish va Mantiq:
871-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #871: http://10.0.1.121:8080 (Og'irlik: 2)
```


# 872-Topshiriq: OpenResty va Nginx Lua arxitekturasi #872
## Topshiriq sharti:
872-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_872 = {
    host = "10.0.1.122",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    872, upstreamNode_872.host, upstreamNode_872.port, upstreamNode_872.weight))
```

## Tushuntirish va Mantiq:
872-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #872: http://10.0.1.122:8080 (Og'irlik: 3)
```


# 873-Topshiriq: OpenResty va Nginx Lua arxitekturasi #873
## Topshiriq sharti:
873-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_873 = {
    host = "10.0.1.123",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    873, upstreamNode_873.host, upstreamNode_873.port, upstreamNode_873.weight))
```

## Tushuntirish va Mantiq:
873-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #873: http://10.0.1.123:8080 (Og'irlik: 4)
```


# 874-Topshiriq: OpenResty va Nginx Lua arxitekturasi #874
## Topshiriq sharti:
874-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_874 = {
    host = "10.0.1.124",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    874, upstreamNode_874.host, upstreamNode_874.port, upstreamNode_874.weight))
```

## Tushuntirish va Mantiq:
874-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #874: http://10.0.1.124:8080 (Og'irlik: 5)
```


# 875-Topshiriq: OpenResty va Nginx Lua arxitekturasi #875
## Topshiriq sharti:
875-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_875 = {
    host = "10.0.1.125",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    875, upstreamNode_875.host, upstreamNode_875.port, upstreamNode_875.weight))
```

## Tushuntirish va Mantiq:
875-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #875: http://10.0.1.125:8080 (Og'irlik: 1)
```


# 876-Topshiriq: OpenResty va Nginx Lua arxitekturasi #876
## Topshiriq sharti:
876-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_876 = {
    host = "10.0.1.126",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    876, upstreamNode_876.host, upstreamNode_876.port, upstreamNode_876.weight))
```

## Tushuntirish va Mantiq:
876-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #876: http://10.0.1.126:8080 (Og'irlik: 2)
```


# 877-Topshiriq: OpenResty va Nginx Lua arxitekturasi #877
## Topshiriq sharti:
877-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_877 = {
    host = "10.0.1.127",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    877, upstreamNode_877.host, upstreamNode_877.port, upstreamNode_877.weight))
```

## Tushuntirish va Mantiq:
877-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #877: http://10.0.1.127:8080 (Og'irlik: 3)
```


# 878-Topshiriq: OpenResty va Nginx Lua arxitekturasi #878
## Topshiriq sharti:
878-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_878 = {
    host = "10.0.1.128",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    878, upstreamNode_878.host, upstreamNode_878.port, upstreamNode_878.weight))
```

## Tushuntirish va Mantiq:
878-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #878: http://10.0.1.128:8080 (Og'irlik: 4)
```


# 879-Topshiriq: OpenResty va Nginx Lua arxitekturasi #879
## Topshiriq sharti:
879-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_879 = {
    host = "10.0.1.129",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    879, upstreamNode_879.host, upstreamNode_879.port, upstreamNode_879.weight))
```

## Tushuntirish va Mantiq:
879-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #879: http://10.0.1.129:8080 (Og'irlik: 5)
```


# 880-Topshiriq: OpenResty va Nginx Lua arxitekturasi #880
## Topshiriq sharti:
880-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_880 = {
    host = "10.0.1.130",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    880, upstreamNode_880.host, upstreamNode_880.port, upstreamNode_880.weight))
```

## Tushuntirish va Mantiq:
880-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #880: http://10.0.1.130:8080 (Og'irlik: 1)
```


# 881-Topshiriq: OpenResty va Nginx Lua arxitekturasi #881
## Topshiriq sharti:
881-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_881 = {
    host = "10.0.1.131",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    881, upstreamNode_881.host, upstreamNode_881.port, upstreamNode_881.weight))
```

## Tushuntirish va Mantiq:
881-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #881: http://10.0.1.131:8080 (Og'irlik: 2)
```


# 882-Topshiriq: OpenResty va Nginx Lua arxitekturasi #882
## Topshiriq sharti:
882-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_882 = {
    host = "10.0.1.132",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    882, upstreamNode_882.host, upstreamNode_882.port, upstreamNode_882.weight))
```

## Tushuntirish va Mantiq:
882-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #882: http://10.0.1.132:8080 (Og'irlik: 3)
```


# 883-Topshiriq: OpenResty va Nginx Lua arxitekturasi #883
## Topshiriq sharti:
883-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_883 = {
    host = "10.0.1.133",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    883, upstreamNode_883.host, upstreamNode_883.port, upstreamNode_883.weight))
```

## Tushuntirish va Mantiq:
883-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #883: http://10.0.1.133:8080 (Og'irlik: 4)
```


# 884-Topshiriq: OpenResty va Nginx Lua arxitekturasi #884
## Topshiriq sharti:
884-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_884 = {
    host = "10.0.1.134",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    884, upstreamNode_884.host, upstreamNode_884.port, upstreamNode_884.weight))
```

## Tushuntirish va Mantiq:
884-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #884: http://10.0.1.134:8080 (Og'irlik: 5)
```


# 885-Topshiriq: OpenResty va Nginx Lua arxitekturasi #885
## Topshiriq sharti:
885-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_885 = {
    host = "10.0.1.135",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    885, upstreamNode_885.host, upstreamNode_885.port, upstreamNode_885.weight))
```

## Tushuntirish va Mantiq:
885-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #885: http://10.0.1.135:8080 (Og'irlik: 1)
```


# 886-Topshiriq: OpenResty va Nginx Lua arxitekturasi #886
## Topshiriq sharti:
886-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_886 = {
    host = "10.0.1.136",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    886, upstreamNode_886.host, upstreamNode_886.port, upstreamNode_886.weight))
```

## Tushuntirish va Mantiq:
886-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #886: http://10.0.1.136:8080 (Og'irlik: 2)
```


# 887-Topshiriq: OpenResty va Nginx Lua arxitekturasi #887
## Topshiriq sharti:
887-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_887 = {
    host = "10.0.1.137",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    887, upstreamNode_887.host, upstreamNode_887.port, upstreamNode_887.weight))
```

## Tushuntirish va Mantiq:
887-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #887: http://10.0.1.137:8080 (Og'irlik: 3)
```


# 888-Topshiriq: OpenResty va Nginx Lua arxitekturasi #888
## Topshiriq sharti:
888-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_888 = {
    host = "10.0.1.138",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    888, upstreamNode_888.host, upstreamNode_888.port, upstreamNode_888.weight))
```

## Tushuntirish va Mantiq:
888-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #888: http://10.0.1.138:8080 (Og'irlik: 4)
```


# 889-Topshiriq: OpenResty va Nginx Lua arxitekturasi #889
## Topshiriq sharti:
889-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_889 = {
    host = "10.0.1.139",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    889, upstreamNode_889.host, upstreamNode_889.port, upstreamNode_889.weight))
```

## Tushuntirish va Mantiq:
889-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #889: http://10.0.1.139:8080 (Og'irlik: 5)
```


# 890-Topshiriq: OpenResty va Nginx Lua arxitekturasi #890
## Topshiriq sharti:
890-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_890 = {
    host = "10.0.1.140",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    890, upstreamNode_890.host, upstreamNode_890.port, upstreamNode_890.weight))
```

## Tushuntirish va Mantiq:
890-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #890: http://10.0.1.140:8080 (Og'irlik: 1)
```


# 891-Topshiriq: OpenResty va Nginx Lua arxitekturasi #891
## Topshiriq sharti:
891-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_891 = {
    host = "10.0.1.141",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    891, upstreamNode_891.host, upstreamNode_891.port, upstreamNode_891.weight))
```

## Tushuntirish va Mantiq:
891-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #891: http://10.0.1.141:8080 (Og'irlik: 2)
```


# 892-Topshiriq: OpenResty va Nginx Lua arxitekturasi #892
## Topshiriq sharti:
892-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_892 = {
    host = "10.0.1.142",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    892, upstreamNode_892.host, upstreamNode_892.port, upstreamNode_892.weight))
```

## Tushuntirish va Mantiq:
892-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #892: http://10.0.1.142:8080 (Og'irlik: 3)
```


# 893-Topshiriq: OpenResty va Nginx Lua arxitekturasi #893
## Topshiriq sharti:
893-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_893 = {
    host = "10.0.1.143",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    893, upstreamNode_893.host, upstreamNode_893.port, upstreamNode_893.weight))
```

## Tushuntirish va Mantiq:
893-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #893: http://10.0.1.143:8080 (Og'irlik: 4)
```


# 894-Topshiriq: OpenResty va Nginx Lua arxitekturasi #894
## Topshiriq sharti:
894-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_894 = {
    host = "10.0.1.144",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    894, upstreamNode_894.host, upstreamNode_894.port, upstreamNode_894.weight))
```

## Tushuntirish va Mantiq:
894-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #894: http://10.0.1.144:8080 (Og'irlik: 5)
```


# 895-Topshiriq: OpenResty va Nginx Lua arxitekturasi #895
## Topshiriq sharti:
895-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_895 = {
    host = "10.0.1.145",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    895, upstreamNode_895.host, upstreamNode_895.port, upstreamNode_895.weight))
```

## Tushuntirish va Mantiq:
895-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #895: http://10.0.1.145:8080 (Og'irlik: 1)
```


# 896-Topshiriq: OpenResty va Nginx Lua arxitekturasi #896
## Topshiriq sharti:
896-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_896 = {
    host = "10.0.1.146",
    port = 8080,
    weight = 2
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    896, upstreamNode_896.host, upstreamNode_896.port, upstreamNode_896.weight))
```

## Tushuntirish va Mantiq:
896-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #896: http://10.0.1.146:8080 (Og'irlik: 2)
```


# 897-Topshiriq: OpenResty va Nginx Lua arxitekturasi #897
## Topshiriq sharti:
897-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_897 = {
    host = "10.0.1.147",
    port = 8080,
    weight = 3
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    897, upstreamNode_897.host, upstreamNode_897.port, upstreamNode_897.weight))
```

## Tushuntirish va Mantiq:
897-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #897: http://10.0.1.147:8080 (Og'irlik: 3)
```


# 898-Topshiriq: OpenResty va Nginx Lua arxitekturasi #898
## Topshiriq sharti:
898-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_898 = {
    host = "10.0.1.148",
    port = 8080,
    weight = 4
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    898, upstreamNode_898.host, upstreamNode_898.port, upstreamNode_898.weight))
```

## Tushuntirish va Mantiq:
898-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #898: http://10.0.1.148:8080 (Og'irlik: 4)
```


# 899-Topshiriq: OpenResty va Nginx Lua arxitekturasi #899
## Topshiriq sharti:
899-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_899 = {
    host = "10.0.1.149",
    port = 8080,
    weight = 5
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    899, upstreamNode_899.host, upstreamNode_899.port, upstreamNode_899.weight))
```

## Tushuntirish va Mantiq:
899-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #899: http://10.0.1.149:8080 (Og'irlik: 5)
```


# 900-Topshiriq: OpenResty va Nginx Lua arxitekturasi #900
## Topshiriq sharti:
900-vazifa: HTTP filtrlari, header manipulyatsiyasi, dinamik marshrutlash va teskari proksi mantig'i.

## Yechim (Lua kodi):
```lua
local upstreamNode_900 = {
    host = "10.0.1.150",
    port = 8080,
    weight = 1
}

print(string.format("Nginx Upstream #%d: http://%s:%d (Og'irlik: %d)", 
    900, upstreamNode_900.host, upstreamNode_900.port, upstreamNode_900.weight))
```

## Tushuntirish va Mantiq:
900-topshiriqda Nginx marshrutlash va muvozanatlash (Load Balancing) tamoyillari ko'rsatildi.

## Ishlash natijasi:
```text
Nginx Upstream #900: http://10.0.1.150:8080 (Og'irlik: 1)
```

