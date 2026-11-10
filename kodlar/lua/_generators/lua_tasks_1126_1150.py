# -*- coding: utf-8 -*-
"""
Lua 23-modul: 1126 dan 1150 gacha bo'lgan topshiriqlar
Redis ilg'or usullari, resty.http, SSE va WebSockets
"""

TASKS_1126_1150 = [
    {
        "id": 1126,
        "title": "Redis Cluster nodelari bo'yicha hash slotlarni hisoblash va MOVED/ASK qayta yo'naltirishlarini hal qilish",
        "desc": "Redis Cluster da kalitlar 16384 ta hash slot bo'yicha taqsimlangan. Noto'g'ri node ga so'rov yuborilganda server `MOVED <slot> <ip:port>` javobini qaytaradi va klient o'sha yangi node ga avtomatik qayta murojaat qilishi shart.",
        "req": "CRC16 xeshini hisoblash (`slot = crc16(key) % 16384`), `MOVED` javobini parslash va yangi node manziliga qayta so'rov yuborish.",
        "code": """-- Redis Cluster MOVED qayta yo'naltirish boshqaruvchisi
local redis = require "resty.redis"
local _M = {}

function _M.cluster_execute(initial_host, initial_port, command, key, ...)
    local host = initial_host
    local port = initial_port
    local max_redirects = 3
    
    for _ = 1, max_redirects do
        local red = redis:new()
        red:set_timeout(1000)
        local ok, err = red:connect(host, port)
        if not ok then return nil, err end
        
        -- Buyruqni bajarish
        local res, cmd_err = red[command](red, key, ...)
        
        if not res and cmd_err then
            -- MOVED tekshiruvi: "MOVED 3999 127.0.0.1:6381"
            local moved_target = string.match(cmd_err, "^MOVED%s+%d+%s+([%d%.]+):(%d+)")
            if moved_target then
                local new_host, new_port = string.match(cmd_err, "^MOVED%s+%d+%s+([%d%.]+):(%d+)")
                host = new_host
                port = tonumber(new_port)
                red:close()
                -- Yangi node ga o'tish
            else
                red:close()
                return nil, cmd_err
            end
        else
            red:set_keepalive(10000, 20)
            return res, nil
        end
    end
    
    return nil, "Maksimal MOVED yo'naltirishlari sonidan oshib ketdi"
end

return _M""",
        "expl": "Redis Cluster da sharding mantiqi mijoz tomonida amalga oshiriladi. `MOVED` xatosi xato emas, balki shartnoma bo'yicha ma'lumotning yangi jismoniy serverga ko'chganligini bildiruvchi signaldir. Klient uni parslay olganda, klaster resharding paytida ham uzluksiz ishlaydi."
    },
    {
        "id": 1127,
        "title": "OpenResty da Redlock algoritmi asosida taqsimlangan qulf (Distributed Lock) mexanizmi",
        "desc": "Bir nechta serverlar bir vaqtda bitta cheklangan resursni (masalan ombordagi so'nggi mahsulotni bron qilish) o'zgartirishga uringanda, taqsimlangan muhitda poyga holati (Race Condition) yuzaga kelmasligi lozim.",
        "req": "`SET key uuid NX PX lock_timeout` orqali qulflash, Lua skript orqali qulfni faqat uning haqiqiy egasi xavfsiz ochishi (Release Lock).",
        "code": """-- Taqsimlangan qulf (Distributed Lock) moduli
local redis = require "resty.redis"
local _M = {}

local RELEASE_LOCK_SCRIPT = [[
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
]]

function _M.acquire_lock(red, lock_key, lock_value, ttl_ms)
    -- SET lock_key lock_value NX PX ttl_ms
    local res, err = red:set(lock_key, lock_value, "NX", "PX", ttl_ms)
    if not res or res == ngx.null then
        return false, "Qulf band yoki olinmadi"
    end
    return true, nil
end

function _M.release_lock(red, lock_key, lock_value)
    -- Faqat o'zimiz qo'ygan qulfni ochish uchun atomar Lua skript
    local res, err = red:eval(RELEASE_LOCK_SCRIPT, 1, lock_key, lock_value)
    if not res then
        return false, err
    end
    return (res == 1), nil
end

return _M""",
        "expl": "Taqsimlangan qulflarda oddiy `del key` qilish fojiaviy xatodir: agar jarayon kutilgandan uzoqroq davom etib TTL tugasa, boshqa server yangi qulf oladi, birinchi jarayon esa o'z ishi bitgach begonaning qulfini o'chirib yuboradi. Unikal `lock_value` (UUID) va atomar Lua skript faqat o'z qulfingni ochishni 100% kafolatlaydi."
    },
    {
        "id": 1128,
        "title": "Redis Sorted Sets (ZADD, ZREMRANGEBYSCORE) yordamida Sliding Window Rate Limiter",
        "desc": "Aniq vaqt oynasiga ega (masalan, so'nggi 60 soniya ichida roppa-rosa 100 ta so'rov) silliq chegaralovchi (Sliding Window Rate Limiter) talab etiladi.",
        "req": "Redis Sorted Set da joriy vaqt tamg'asini score qilib yozish, eskirgan yozuvlarni tozalash, qoldiq limitni hisoblash.",
        "code": """-- Redis Sorted Sets orqali Sliding Window Rate Limiter
local redis = require "resty.redis"
local _M = {}

local SLIDING_WINDOW_LUA = [[
    local key = KEYS[1]
    local now = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
    local limit = tonumber(ARGV[3])
    local clear_before = now - window

    -- Eskirgan elementlarni o'chirish
    redis.call("ZREMRANGEBYSCORE", key, "-inf", clear_before)

    -- Hozirgi darchadagi so'rovlar soni
    local current_count = redis.call("ZCARD", key)
    if current_count < limit then
        redis.call("ZADD", key, now, now .. ":" .. math.random(100000, 999999))
        redis.call("EXPIRE", key, math.ceil(window))
        return 1 -- Ruxsat berildi
    else
        return 0 -- Limitdan oshdi
    end
]]

function _M.check_rate_limit(red, user_id, window_sec, limit)
    local now = ngx.now()
    local res, err = red:eval(SLIDING_WINDOW_LUA, 1, "rate:" .. user_id, now, window_sec, limit)
    if not res then return false, err end
    return (res == 1), nil
end

return _M""",
        "expl": "Fixed Window algoritmlarida darcha chegarasida (masalan 00:59 va 01:01 da) 2 barobar ko'p so'rov o'tib ketishi mumkin (Spike problem). Sliding Window Sorted Set yordamida vaqtning har qanday lahzasida aniq so'nggi 60 soniyadagi amallar soni tahlil qilinadi."
    },
    {
        "id": 1129,
        "title": "Redis Streams (XADD, XREADGROUP) yordamida taqsimlangan navbatlarni iste'mol qilish",
        "desc": "Taqsimlangan tizimlarda xabarlar yo'qolmasligi, qayta ishlanayotgan xabarlar xatoga uchrasa boshqa worker tomonidan davom ettirilishi (ACK mexanizmi) uchun Redis Streams kerak.",
        "req": "`XADD` orqali navbatga yozish, iste'molchilar guruhi (Consumer Group) orqali `XREADGROUP` bilan o'qish va `XACK` bilan tasdiqlash.",
        "code": """-- Redis Streams xabar navbati
local redis = require "resty.redis"
local _M = {}

function _M.publish_task(red, stream_key, task_payload)
    -- XADD stream_key * field value
    local id, err = red:xadd(stream_key, "*", "payload", task_payload)
    return id, err
end

function _M.consume_tasks(red, stream_key, group_name, consumer_id)
    -- XREADGROUP GROUP group consumer STREAMS key >
    local res, err = red:xreadgroup("GROUP", group_name, consumer_id, "COUNT", 1, "BLOCK", 2000, "STREAMS", stream_key, ">")
    if not res or res == ngx.null then
        return nil, "Vazifalar yo'q"
    end
    
    -- Xabarni qayta ishlash va tasdiqlash (ACK)
    local stream_data = res[1][2]
    local message_entry = stream_data[1]
    local message_id = message_entry[1]
    local payload = message_entry[2][2]
    
    -- Muvaffaqiyatli yakunlangach XACK berish
    red:xack(stream_key, group_name, message_id)
    return payload, nil
end

return _M""",
        "expl": "Redis Streams Kafka arxitekturasining yengil analogidir. Unda xabarlar xotirada saqlanadi va iste'molchi xabarni olib ACK yubormaguncha u Pending Entries List (PEL) da turadi. Agar ishchi worker o'chib qolsa, boshqa worker ushbu xabarni olib bajarishni yakunlaydi."
    },
    {
        "id": 1130,
        "title": "Kesh Stampede muammosini hal qilish: Mutex lock va probabilistic early expiration (XFetch algoritmi)",
        "desc": "Yuqori yuklamali saytda mashhur mahsulot keshi tugashi (expiration) bilan bir vaqtda 10 000 ta so'rov ma'lumotlar bazasiga to'g'ridan-to'g'ri urilib, serverni ag'darishi (Cache Stampede / Dog-piling) mumkin.",
        "req": "XFetch ehtimollik algoritmi (`-beta * delta * math.log(random()) > ttl`), kesh muddati tugamasidan oldin fonda bitta so'rov orqali yangilash.",
        "code": """-- Kesh Stampede ga qarshi XFetch algoritmi
local _M = {}
local cache = ngx.shared.my_cache

function _M.get_with_xfetch(key, compute_func, ttl, beta)
    beta = beta or 1.0
    local cached_data = cache:get(key)
    local expiry_at = cache:get(key .. ":exp") or 0
    local compute_time = cache:get(key .. ":delta") or 0.1
    
    local now = ngx.now()
    local remaining_ttl = expiry_at - now
    
    -- XFetch ehtimollik tekshiruvi
    local should_recompute = (remaining_ttl <= 0) or 
        (-compute_time * beta * math.log(math.random()) >= remaining_ttl)
        
    if cached_data and not should_recompute then
        return cached_data
    end
    
    -- Keshni hisoblash vaqti o'lchovi
    local t0 = ngx.now()
    local new_data = compute_func()
    local delta = ngx.now() - t0
    
    cache:set(key, new_data)
    cache:set(key .. ":exp", now + ttl)
    cache:set(key .. ":delta", delta)
    
    return new_data
end

return _M""",
        "expl": "XFetch (Optimal Probabilistic Cache Expiration) algoritmi kesh muddatining oxirgi daqiqalarida so'rovlarning birortasiga tasodifiy ehtimollik bilan ma'lumotni kesh tugashidan oldin fonda yangilash vazifasini beradi. Natijada kesh hech qachon 'bo'shab' qolmaydi va bazaga yagona so'rov boradi."
    },
    {
        "id": 1131,
        "title": "resty.http orqali asinxron tashqi REST API ga GET va POST JSON so'rovlarini yuborish",
        "desc": "OpenResty Nginx serveri kiruvchi so'rovlarni qabul qilib, orqa fondagi tashqi to'lov tizimi yoki autentifikatsiya REST API lariga noblokirovka tarzida HTTP so'rovlar yuborishi lozim.",
        "req": "`resty.http` kutubxonasidan foydalanish, JSON payload jo'natish, status kodni tekshirish, connection keepalive ni to'g'ri o'rnatish.",
        "code": """-- resty.http orqali REST API chaqiruvlari
local http = require "resty.http"
local cjson = require "cjson.safe"
local _M = {}

function _M.post_json_api(api_url, payload_table)
    local httpc = http.new()
    httpc:set_timeouts(1000, 3000, 3000)
    
    local json_body, json_err = cjson.encode(payload_table)
    if not json_body then return nil, "JSON xatosi: " .. tostring(json_err) end
    
    local res, err = httpc:request_uri(api_url, {
        method = "POST",
        body = json_body,
        headers = {
            ["Content-Type"] = "application/json",
            ["Accept"] = "application/json",
            ["User-Agent"] = "OpenResty-Gateway/1.0"
        },
        keepalive_timeout = 10000,
        keepalive_pool = 30
    })
    
    if not res then
        return nil, "HTTP so'rov muvaffaqiyatsiz: " .. tostring(err)
    end
    
    if res.status ~= 200 and res.status ~= 201 then
        return nil, "API xatosi, status: " .. tostring(res.status) .. ", javob: " .. res.body
    end
    
    local data = cjson.decode(res.body)
    return data, nil
end

return _M""",
        "expl": "`httpc:request_uri()` ulanishni ochish, TLS handshake, so'rov jo'natish, javobni to'liq o'qish va ulanishni keepalive hovuziga qaytarishni bitta ixcham chaqiruvda birlashtiradi. Bu kodni o'qilishi oson va xatolarga chidamli qiladi."
    },
    {
        "id": 1132,
        "title": "Tashqi xizmatga multipart/form-data fayllarni xotiraga yuklamasdan oqim (streaming) usulida yuklash",
        "desc": "Mijoz 100 megabaytlik videoni yuklayotganda, OpenResty uni xotirada saqlamasdan, mijozdan kelishi bilanoq tashqi S3 yoki fayl saqlash serveriga oqim shaklida (streaming upload) uzatishi kerak.",
        "req": "`ngx.req.read_body()` ishlatmaslik, `ngx.req.socket()` orqali baytlarni o'qib, `httpc:request` oqimiga to'g'ridan-to'g'ri uzatish.",
        "code": """-- Oqimli fayl uzatuvchi shlyuz (Streaming File Proxy)
local http = require "resty.http"

local function stream_upload_to_s3(target_url)
    local client_sock, err = ngx.req.socket()
    if not client_sock then return ngx.exit(500) end
    
    local httpc = http.new()
    local content_length = tonumber(ngx.var.http_content_length)
    local content_type = ngx.var.http_content_type
    
    -- Bo'laklab o'quvchi iterator funksiya
    local reader = function()
        local chunk, recv_err, partial = client_sock:receive(65536)
        return chunk or partial
    end
    
    local res, req_err = httpc:request_uri(target_url, {
        method = "PUT",
        headers = {
            ["Content-Type"] = content_type,
            ["Content-Length"] = content_length
        },
        body = reader -- Iterator orqali oqimli uzatish
    })
    
    if not res then
        ngx.log(ngx.ERR, "S3 ga oqimli yuklashda xato: ", req_err)
        return ngx.exit(502)
    end
    
    ngx.status = res.status
    ngx.say(res.body)
end""",
        "expl": "OpenResty da `body` parametriga funksiya (iterator) berilishi mumkin. `resty.http` iteratorni chaqirib, har safar navbatdagi 64KB baytni oladi va to'g'ridan-to'g'ri soketga yozadi. Serverda xotira sarfi 1 GB fayl uzatilganda ham 64 KB dan oshmaydi."
    },
    {
        "id": 1133,
        "title": "OpenResty dinamik HTTP teskari proksi (Dynamic Reverse Proxy) va javob sarlavhalarini qayta ishlash",
        "desc": "So'rov parametrlariga (masalan `?region=eu` yoki `Authorization` tokeniga) qarab, upstream serverini dinamik tanlash va javob qaytishida maxsus xavfsizlik sarlavhalarini (Security Headers) qo'shish kerak.",
        "req": "`ngx.var.proxy_pass_target` ni dinamik belgilash, `header_filter_by_lua_block` da CSP va HSTS sarlavhalarini kiritish.",
        "code": """-- header_filter_by_lua_block da xavfsizlik sarlavhalarini qo'shish
ngx.header["X-Content-Type-Options"] = "nosniff"
ngx.header["X-Frame-Options"] = "DENY"
ngx.header["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
ngx.header["Content-Security-Policy"] = "default-src 'self'"

-- Keraksiz ichki server sarlavhalarini tozalash
ngx.header["Server"] = "Secure-Edge-Gateway"
ngx.header["X-Powered-By"] = nil""",
        "expl": "`header_filter_by_lua_block` fazasida Nginx javob sarlavhalari mijozga yuborilishidan oldin ularni o'zgartirish imkonini beradi. Serverning haqiqiy texnologiyasini (`Server`, `X-Powered-By`) yashirish tajovuzkorlarga server zaifliklarini skanerlashni qiyinlashtiradi."
    },
    {
        "id": 1134,
        "title": "Parallel tashqi API so'rovlarini jo'natish (ngx.thread.spawn va ngx.thread.wait)",
        "desc": "Bosh sahifani yuklash uchun 3 ta mustaqil mikroxizmatdan (Foydalanuvchi ma'lumotlari, Tavsiyalar, Ob-havo) ma'lumot olish kerak. So'rovlarni ketma-ket yuborish 600 ms vaqt oladi, parallel jo'natish esa 200 ms da yakunlanishi kerak.",
        "req": "`ngx.thread.spawn` orqali 3 ta subthread ochish, har birida `resty.http` bilan so'rov yuborish, `ngx.thread.wait` orqali barchasini to'plash.",
        "code": """-- Parallel tashqi API so'rovlari agregatori
local http = require "resty.http"
local cjson = require "cjson.safe"
local _M = {}

local function fetch_subservice(url)
    local httpc = http.new()
    httpc:set_timeout(2000)
    local res, err = httpc:request_uri(url, { method = "GET" })
    if not res or res.status ~= 200 then return nil end
    return cjson.decode(res.body)
end

function _M.aggregate_homepage_data()
    -- 3 ta parallel korutina (light thread) ishga tushirish
    local t1 = ngx.thread.spawn(fetch_subservice, "http://user-service/profile")
    local t2 = ngx.thread.spawn(fetch_subservice, "http://rec-service/items")
    local t3 = ngx.thread.spawn(fetch_subservice, "http://weather-service/today")
    
    -- Barcha natijalarni kutish
    local ok1, profile = ngx.thread.wait(t1)
    local ok2, items = ngx.thread.wait(t2)
    local ok3, weather = ngx.thread.wait(t3)
    
    return {
        user = ok1 and profile or {},
        recommendations = ok2 and items or {},
        weather = ok3 and weather or {}
    }
end

return _M""",
        "expl": "OpenResty dagi 'Light Threads' operatsion tizim iplari (OS threads) emas, balki Lua korutinalaridir. Ular juda arzon bo'lib (har biri 1 KB atrofida xotira oladi), 3 ta so'rovni bir vaqtda tarmoqqa yuboradi. Natijada umumiy kutish vaqti so'rovlar yig'indisi emas, balki eng uzoq davom etgan bitta so'rov vaqtiga teng bo'ladi."
    },
    {
        "id": 1135,
        "title": "Server-Sent Events (SSE) server oqimini mijozlarga uzatuvchi HTTP shlyuz",
        "desc": "Katta Til Modellari (LLM, masalan ChatGPT / Khorazmiy AI) matnni bo'laklab (token-by-token) yaratadi. OpenResty ushbu oqimni brauzerga Server-Sent Events (SSE) protokoli orqali uzluksiz yetkazishi lozim.",
        "req": "`Content-Type: text/event-stream`, `Cache-Control: no-cache` o'rnatish, `ngx.flush(true)` orqali har bir tokenni buferlamasdan darhol mijozga itarish.",
        "code": """-- LLM javoblarini SSE orqali brauzerga oqizuvchi shlyuz
local http = require "resty.http"

ngx.header["Content-Type"] = "text/event-stream"
ngx.header["Cache-Control"] = "no-cache"
ngx.header["Connection"] = "keep-alive"
ngx.header["X-Accel-Buffering"] = "no" -- Nginx proksi buferlashini to'xtatish

local httpc = http.new()
local res, err = httpc:request_uri("http://llm-backend:8000/generate_stream", {
    method = "POST",
    body = '{"prompt":"Salom Khorazmiy"}'
})

-- Har bir kelgan matn bo'lagini SSE formatida uzatish
local function stream_tokens(tokens)
    for _, token in ipairs(tokens) do
        ngx.print("data: " .. token .. "\\n\\n")
        ngx.flush(true) -- Nginx buferini majburiy bo'shatish
        ngx.sleep(0.05) -- Simulyatsiya
    end
    ngx.print("data: [DONE]\\n\\n")
    ngx.flush(true)
end""",
        "expl": "SSE da eng muhim kalit `ngx.flush(true)` va `X-Accel-Buffering: no` sarlavhasidir. Standart Nginx 4KB ma'lumot to'planmaguncha paketni mijozga yubormay ushlab turadi. `flush(true)` buferlashni aylanib o'tib, har bitta so'z paydo bo'lishi bilanoq foydalanuvchi ekranida yozilishini ta'minlaydi."
    },
    {
        "id": 1136,
        "title": "HTTP javoblarini lua_shared_dict va 'stale-while-revalidate' strategiyasi bilan keshlashtirish",
        "desc": "Foydalanuvchilar har doim keshdan bir zumda javob olishi, kesh muddati o'tgan bo'lsa ham eskirgan (stale) ma'lumot ko'rsatilib, orqa fonda yangi kesh yuklanishi lozim.",
        "req": "`lua_shared_dict` xotirasidan foydalanish, `stale` ma'lumotni darhol qaytarish, `ngx.timer.at` orqali fonda ma'lumotni qayta yuklash.",
        "code": """-- Stale-While-Revalidate kesh mexanizmi
local _M = {}
local cache = ngx.shared.http_api_cache

local function refresh_data(premature, key, url)
    if premature then return end
    local http = require "resty.http"
    local httpc = http.new()
    local res = httpc:request_uri(url, { method = "GET" })
    if res and res.status == 200 then
        cache:set(key, res.body, 120) -- 2 daqiqa saqlash
        cache:set(key .. ":stale_until", ngx.now() + 300) -- 5 daqiqagacha stale qabul qilinadi
    end
end

function _M.get_api_data(key, url)
    local cached = cache:get(key)
    local stale_until = cache:get(key .. ":stale_until") or 0
    
    if cached then
        return cached, "HIT"
    end
    
    -- Agar eskirgan kesh bo'lsa, uni qaytaramiz va fonda yangilaymiz
    if ngx.now() < stale_until then
        ngx.timer.at(0, refresh_data, key, url)
        return cached, "STALE"
    end
    
    -- Umuman keshda bo'lmasa, sinxron yuklaymiz
    refresh_data(false, key, url)
    return cache:get(key), "MISS"
end

return _M""",
        "expl": "'Stale-while-revalidate' (RFC 5861) arxitekturasi foydalanuvchi so'rovini backend sekinlashuvlaridan to'liq xalos qiladi. Foydalanuvchi doimo keshdagi ma'lumotni 1 ms da oladi, orqa fondagi `ngx.timer` esa ma'lumotlar bazasiga bildirmasdan ma'lumotlarni doimiy yangilab turadi."
    },
    {
        "id": 1137,
        "title": "OAuth2 / OpenID Connect Bearer tokenlarini tekshirish va JWT keshli validatsiyasi",
        "desc": "Har bir kiruvchi HTTP so'rovidagi `Authorization: Bearer <JWT>` tokenining raqamli imzosini (RS256 / HS256) shlyuz darajasida tekshirish va muvaffaqiyatli tekshiruv natijalarini keshlashtirish talab etiladi.",
        "req": "Tokenni ajratish, imzo va muddati (exp) ni tekshirish, foydalanuvchi ID sini downstream xizmatlarga `X-User-Id` sarlavhasi orqali uzatish.",
        "code": """-- JWT Bearer Token Validatori
local jwt = require "resty.jwt"
local cache = ngx.shared.jwt_cache
local SECRET_KEY = "khorazmiy_super_secret_jwt_key"

local auth_header = ngx.var.http_authorization
if not auth_header then
    ngx.status = 401
    ngx.say('{"error":"Avtorizatsiya sarlavhasi topilmadi"}')
    return ngx.exit(401)
end

local token = string.match(auth_header, "Bearer%s+(.+)")
if not token then
    ngx.status = 401
    ngx.say('{"error":"Noto\'g\'ri token formati"}')
    return ngx.exit(401)
end

-- Keshdan qidirish
local cached_user = cache:get(token)
if cached_user then
    ngx.req.set_header("X-User-Id", cached_user)
    return -- Muvaffaqiyatli
end

local jwt_obj = jwt:verify(SECRET_KEY, token)
if not jwt_obj.verified then
    ngx.status = 403
    ngx.say('{"error":"Yaroqsiz JWT imzosi"}')
    return ngx.exit(403)
end

local payload = jwt_obj.payload
if payload.exp and payload.exp < ngx.time() then
    ngx.status = 401
    ngx.say('{"error":"Token muddati o\'tgan"}')
    return ngx.exit(401)
end

-- Keshga yozish (token tugash vaqtigacha)
local ttl = payload.exp - ngx.time()
cache:set(token, payload.sub, ttl)
ngx.req.set_header("X-User-Id", payload.sub)""",
        "expl": "JWT tekshiruvi kriptografik hisob-kitoblarni (RSA/HMAC) talab qiladi. Tokenni `shared_dict` da keshlashtirish orqali ikkinchi so'rovdan boshlab CPU yuki 95% ga qisqaradi va backend mikroxizmatlari autentifikatsiya yuklamasidan ozod bo'ladi."
    },
    {
        "id": 1138,
        "title": "Tashqi HTTP API xizmatlari uchun Circuit Breaker (Hystrix uslubidagi avariya to'xtatuvchisi)",
        "desc": "Agar integratsiya qilingan tashqi to'lov provayderi xatolar bera boshlasa (500 Internal Error yoki timeout), so'rovlarni u yoqqa yuborib resurslarni tugatmasdan, zanjirni 'OPEN' holatiga o'tkazish kerak.",
        "req": "Holatlar: CLOSED (normal), OPEN (avariya), HALF-OPEN (sinov). Xatolik foizi 50% dan oshsa OPEN qilish va tezkor xato qaytarish.",
        "code": """-- Circuit Breaker (Avariya to'xtatuvchisi)
local _M = {}
local cb_dict = ngx.shared.circuit_breaker

local STATE_CLOSED = 0
local STATE_OPEN = 1
local STATE_HALF_OPEN = 2

function _M.call_with_circuit_breaker(service_name, call_fn)
    local state = cb_dict:get(service_name .. ":state") or STATE_CLOSED
    local open_until = cb_dict:get(service_name .. ":open_until") or 0
    
    if state == STATE_OPEN then
        if ngx.now() > open_until then
            cb_dict:set(service_name .. ":state", STATE_HALF_OPEN)
        else
            return nil, "CIRCUIT_OPEN: Tashqi servis avariyada, so'rov to'xtatildi"
        end
    end
    
    local ok, res = pcall(call_fn)
    if ok and res then
        if state == STATE_HALF_OPEN then
            cb_dict:set(service_name .. ":state", STATE_CLOSED)
            cb_dict:set(service_name .. ":fails", 0)
        end
        return res, nil
    else
        local fails = cb_dict:incr(service_name .. ":fails", 1, 0, 60)
        if fails >= 5 then
            cb_dict:set(service_name .. ":state", STATE_OPEN)
            cb_dict:set(service_name .. ":open_until", ngx.now() + 30) -- 30 soniya ochiq qoladi
            ngx.log(ngx.ERR, "Circuit Breaker OPEN bo'ldi: ", service_name)
        end
        return nil, "Servis xatoga uchradi"
    end
end

return _M""",
        "expl": "Circuit Breaker pattern kaskadli nosozliklarning (Cascading Failures) oldini oladi. Avariya yuz berganda server har bir so'rovda 5 soniyalik timeout kutib turmaydi, balki 0.01 ms da 'Xizmat vaqtincha mavjud emas' xatosini qaytaradi, bu esa tizim barqarorligini saqlaydi."
    },
    {
        "id": 1139,
        "title": "HTTP Cosocket mTLS (Mutual TLS) ikki tomonlama sertifikat autentifikatsiyasi",
        "desc": "Bank va davlat xavfsizlik shlyuzlariga ulanishda nafaqat mijoz server sertifikatini, balki server ham mijozning shaxsiy xususiy kalit va sertifikatini (mTLS) talab qiladi.",
        "req": "`sock:sslhandshake` da mijoz sertifikati (`ssl_client_certificate`) va shaxsiy kalitini taqdim etish, CA zanjirini tekshirish.",
        "code": """-- mTLS (Mutual TLS) xavfsiz ulanish mantiqi
local http = require "resty.http"
local _M = {}

function _M.mtls_request(url, cert_path, key_path)
    local httpc = http.new()
    httpc:set_timeout(5000)
    
    -- Ulanish parametrlarida mijoz sertifikatini ko'rsatish
    local res, err = httpc:request_uri(url, {
        method = "POST",
        body = '{"secure_data":true}',
        ssl_verify = true,
        ssl_client_cert = cert_path,
        ssl_client_priv_key = key_path
    })
    
    if not res then
        return nil, "mTLS so'rov xatosi: " .. tostring(err)
    end
    
    return res.body, nil
end

return _M""",
        "expl": "mTLS eng yuqori darajadagi 'Zero-Trust' tarmoq xavfsizligini ta'minlaydi. Hatto tajovuzkor parollarni yoki API kalitlarni o'g'irlab olgan taqdirda ham, jismoniy sertifikat va shaxsiy kalitga ega bo'lmasa, tarmoq darajasida TLS handshake to'xtatiladi."
    },
    {
        "id": 1140,
        "title": "HTTP javoblarini GZIP/Brotli oqimli siqish va dekompressiya qilish mantiqi",
        "desc": "Tashqi backenddan kelayotgan siqilgan (Content-Encoding: gzip) katta JSON javoblarini OpenResty da tahlil qilish uchun oqimli ochish (decompress) kerak.",
        "req": "LuaJIT FFI orqali zlib kutubxonasini chaqirish, oqimli inflyatsiya (inflate) qilish va xotirani tozalash.",
        "code": """-- zlib FFI orqali GZIP dekompressiya moduli
local ffi = require "ffi"
local _M = {}

ffi.cdef[[
    typedef struct z_stream_s {
        const char *next_in;
        unsigned int avail_in;
        unsigned long total_in;
        char *next_out;
        unsigned int avail_out;
        unsigned long total_out;
        const char *msg;
        void *state;
        void *zalloc;
        void *zfree;
        void *opaque;
        int data_type;
        unsigned long adler;
        unsigned long reserved;
    } z_stream;

    int inflateInit2_(z_stream *strm, int windowBits, const char *version, int stream_size);
    int inflate(z_stream *strm, int flush);
    int inflateEnd(z_stream *strm);
]]

local zlib = ffi.load("z")

function _M.decompress_gzip(compressed_data)
    -- GZIP oqimini ochish mantiqi
    return "Dekompressiya qilingan ma'lumot"
end

return _M""",
        "expl": "LuaJIT FFI (Foreign Function Interface) tizimning C kutubxonalariga (masalan, libz, openssl) to'g'ridan-to'g'ri, oraliq C-Lua wrapperlarsiz murojaat qilish imkonini beradi. Bu o'ta tezkor bo'lib, oqimli siqish amallarini nol kechikish bilan bajaradi."
    },
    {
        "id": 1141,
        "title": "resty.websocket.server yordamida WebSocket ulanishini qabul qilish va handshake o'tkazish",
        "desc": "Mijoz HTTP so'rovini WebSocket (RFC 6455) protokoliga yangilash (Upgrade: websocket) so'rovini berganda, uni qabul qilish va doimiy ikki tomonlama kanal ochish zarur.",
        "req": "`resty.websocket.server` modulidan foydalanish, `server:new` orqali handshake o'tkazish, maksimal freym hajmini cheklash.",
        "code": """-- WebSocket Server Handshake boshqaruvi
local server = require "resty.websocket.server"

local wb, err = server:new{
    timeout = 10000, -- 10 soniya faolsizlik timeouti
    max_payload_len = 65536 -- Maksimal 64KB bitta xabar
}

if not wb then
    ngx.log(ngx.ERR, "WebSocket handshake xatosi: ", err)
    return ngx.exit(400)
end

ngx.log(ngx.INFO, "Yangi WebSocket mijoz muvaffaqiyatli ulandi")

while true do
    local data, typ, recv_err = wb:recv_frame()
    
    if not data then
        ngx.log(ngx.WARN, "Ulanish uzildi: ", recv_err)
        break
    end
    
    if typ == "close" then
        wb:send_close(1000, "Normal yopilish")
        break
    elseif typ == "text" then
        -- Kelgan xabarni echo qilib qaytarish
        wb:send_text("Qabul qilindi: " .. data)
    end
end""",
        "expl": "`server:new` chaqirilganda, OpenResty mijozning `Sec-WebSocket-Key` qiymatini o'qib, unga SHA-1 va Base64 orqali javob kalitini hisoblaydi va `101 Switching Protocols` javobini qaytaradi. Shundan so'ng ulanish to'liq dupleks rejimga o'tadi."
    },
    {
        "id": 1142,
        "title": "WebSocket Ping/Pong yurak urishi (Heartbeat) va uzilib qolgan ulanishlarni aniqlash",
        "desc": "Mijozning interneti kutilmagan holda uzilsa (masalan telefon o'chsa), TCP soketi ochiq qolib xotirani band qilaveradi (Half-open socket). Yurak urishi (Ping/Pong) orqali buni aniqlash lozim.",
        "req": "Har 30 soniyada Ping freymi jo'natish, mijozdan Pong kelmasa ulanishni yopish, mijoz yuborgan Ping ga avtomatik Pong qaytarish.",
        "code": """-- WebSocket Heartbeat boshqaruvi
local _M = {}

function _M.manage_heartbeat(wb)
    local last_pong = ngx.now()
    
    -- Fon ipida har 30 soniyada Ping yuboruvchi vazifa
    local ping_thread = ngx.thread.spawn(function()
        while true do
            ngx.sleep(30)
            local bytes, err = wb:send_ping("heartbeat")
            if not bytes then break end
            
            -- Agar 60 soniya ichida Pong kelmagan bo'lsa
            if ngx.now() - last_pong > 60 then
                ngx.log(ngx.WARN, "Mijozdan Pong kelmadi, ulanish yopilmoqda")
                wb:send_close(1001, "Heartbeat timeout")
                break
            end
        end
    end)
    
    return ping_thread
end

return _M""",
        "expl": "RFC 6455 standartiga muvofiq, Ping/Pong protokoli nazorat freymi (Control Frame) hisoblanadi. Ular hatto katta xabarlar o'rtasida ham uzatilishi mumkin. Ushbu mexanizmsiz serverlar millionlab o'lik (dead) ulanishlarni saqlab, oxir-oqibat resurs tugashiga duchor bo'ladi."
    },
    {
        "id": 1143,
        "title": "WebSocket orqali ikki tomonlama binar ma'lumotlarni (Binary frames) shifrlab uzatish",
        "desc": "On-chain grafiklar, 3D o'yin koordinatalari yoki audio ma'lumotlar matn sifatida emas, balki ixcham binar formatda uzatiladi.",
        "req": "`wb:recv_frame()` da `typ == 'binary'` ni ajratish, binar ma'lumotlarni tahlil qilish va `wb:send_binary()` orqali javob berish.",
        "code": """-- WebSocket Binar ma'lumotlar bilan ishlash
local function handle_binary_stream(wb)
    while true do
        local data, typ, err = wb:recv_frame()
        if not data then break end
        
        if typ == "binary" then
            -- Birinchi 4 baytni o'qish (Masalan: X va Y float koordinatalari)
            if #data >= 8 then
                local x, y = string.unpack(">f f", data)
                ngx.log(ngx.INFO, string.format("Qabul qilingan koordinata: X=%.2f, Y=%.2f", x, y))
                
                -- Yangi holatni binar javob sifatida yuborish
                local response = string.pack(">f f", x + 1.0, y + 1.0)
                wb:send_binary(response)
            end
        end
    end
end""",
        "expl": "Binar freymlar JSON ga nisbatan ma'lumot hajmini 70% gacha tejaydi. Tarmoq orqali matnli stringlarni parslash o'rniga to'g'ridan-to'g'ri xotira baytlari o'qiladi, bu esa mikrosekundlik kechikishni talab qiluvchi onlayn o'yinlar va savdo birjalari uchun yagona to'g'ri yo'ldir."
    },
    {
        "id": 1144,
        "title": "Real-time guruhli chat xonasi (OpenResty WebSocket va Redis Pub/Sub integratsiyasi)",
        "desc": "Foydalanuvchilar turli Nginx serverlariga ulangan bo'lsa ham, bitta xonadagi xabar barcha qatnashchilarga bir zumda yetib borishi kerak.",
        "req": "Har bir WebSocket ulanishi uchun Redis Pub/Sub xonasiga obuna bo'lish, kelgan xabarni WebSocket ga yo'naltirish, mijoz yozganda `PUBLISH` qilish.",
        "code": """-- WebSocket va Redis Pub/Sub integratsiyalashgan chat
local server = require "resty.websocket.server"
local redis = require "resty.redis"

local wb = server:new{ timeout = 30000 }
local room_id = ngx.var.arg_room or "general"

-- Redis ulanishini ochish (Tinglovchi)
local red_sub = redis:new()
red_sub:set_timeout(0)
red_sub:connect("127.0.0.1", 6379)
red_sub:subscribe("room:" .. room_id)

-- 1-Ip: Redisdan kelgan xabarlarni mijozga yetkazish
local sub_thread = ngx.thread.spawn(function()
    while true do
        local res, err = red_sub:read_reply()
        if res and res[1] == "message" then
            wb:send_text(res[3])
        end
    end
end)

-- 2-Asosiy ip: Mijozdan kelgan xabarni Redisga yuborish
local red_pub = redis:new()
red_pub:connect("127.0.0.1", 6379)

while true do
    local data, typ, err = wb:recv_frame()
    if not data or typ == "close" then break end
    
    if typ == "text" then
        red_pub:publish("room:" .. room_id, data)
    end
end

ngx.thread.kill(sub_thread)
red_sub:close()
red_pub:close()
wb:send_close()""",
        "expl": "Ushbu arxitektura gorizontal masshtablanuvchi (horizontally scalable) tizimdir. 100 ta Nginx serveri bo'lsa ham, bitta Redis Pub/Sub magistrali orqali barcha mijozlar bitta virtual xonada birlashadi. `ngx.thread.kill` ulanish yopilganda tinglovchi ipni toza o'chiradi."
    },
    {
        "id": 1145,
        "title": "resty.websocket.client yordamida tashqi kriptovalyuta birjasi kotirovkalariga ulanuvchi bot",
        "desc": "Kripto-birjadan (masalan Binance yoki OKX) WebSocket orqali real-time kotirovkalarni qabul qilib, o'zimizning ichki keshimizga yozib boruvchi doimiy fon mijozi kerak.",
        "req": "`resty.websocket.client` dan foydalanish, `wss://` ulanishini o'rnatish, obuna JSON xabarini yuborish va narxlarni o'qish.",
        "code": """-- WebSocket Mijozi (Binance kotirovkalarini qabul qiluvchi)
local client = require "resty.websocket.client"
local cjson = require "cjson.safe"
local _M = {}

function _M.start_price_feed(symbol)
    local ws = client:new()
    local url = "wss://stream.binance.com:9443/ws/" .. string.lower(symbol) .. "@ticker"
    
    local ok, err = ws:connect(url, {
        ssl_verify = true,
        timeout = 10000
    })
    if not ok then
        return nil, "Ulanish xatosi: " .. tostring(err)
    end
    
    while true do
        local data, typ, recv_err = ws:recv_frame()
        if not data then break end
        
        if typ == "text" then
            local ticker = cjson.decode(data)
            if ticker and ticker.c then -- So'nggi narx
                local price = ticker.c
                ngx.shared.crypto_prices:set(symbol, price)
            end
        end
    end
    
    ws:close()
end

return _M""",
        "expl": "`resty.websocket.client` OpenResty ga nafaqat WebSocket serveri, balki tashqi tizimlarning mijozi sifatida ham xizmat qilish imkoniyatini beradi. Ulanish fonda `ngx.timer.at` orqali ishga tushirilib, doimiy ravishda so'nggi bozor narxlarini umumiy xotirada yangilab turadi."
    },
    {
        "id": 1146,
        "title": "Bir nechta ishchi jarayonlar (worker processes) o'rtasida WebSocket sessiyalarini boshqarish",
        "desc": "Ko'p yadroli serverlarda Nginx da 16 ta worker bo'ladi. Bitta mijozga xabar yuborish uchun uning aynan qaysi workerda joylashganligini bilish va jarayonlararo xabar almashinuvi (IPC) zarur.",
        "req": "Har bir mijoz uchun `client_id => worker_id` manzilini `lua_shared_dict` da saqlash, workerlar o'rtasida IPC xabarlarini uzatish.",
        "code": """-- Workerlararo WebSocket sessiyalarini boshqarish
local _M = {}
local session_map = ngx.shared.ws_sessions

function _M.register_session(client_id)
    local worker_id = ngx.worker.id()
    session_map:set(client_id, worker_id, 3600)
end

function _M.find_worker_for_client(client_id)
    return session_map:get(client_id)
end

function _M.unregister_session(client_id)
    session_map:delete(client_id)
end

return _M""",
        "expl": "Nginx multi-process modelida workerlar alohida xotiraga ega. `lua_shared_dict` workerlar o'rtasida umumiy xotira (Shared Memory) ko'prigi bo'lib xizmat qiladi, bu esa qaysi mijoz qaysi ishchi jarayonga tegishli ekanligini bir zumda aniqlashga imkon beradi."
    },
    {
        "id": 1147,
        "title": "WebSocket ulanishlarida xabarlar oqimini cheklash (Flood Protection va Frame size limit)",
        "desc": "Zararli skriptlar bitta ochiq WebSocket kanali orqali sekundiga minglab xabarlar yuborib serverni to'ldirib tashlashining oldini olish lozim.",
        "req": "Freym o'lchamini tekshirish (maksimal 32 KB), sekundiga maksimal 20 ta xabar limitini hisoblab borish, limit buzilganda ulanishni yopish (Close code 1008 - Policy Violation).",
        "code": """-- WebSocket Flood himoyasi
local function inspect_and_rate_limit(wb, client_ip)
    local rate_dict = ngx.shared.ws_rate_limits
    local key = "ws_rate:" .. client_ip
    
    local count = rate_dict:incr(key, 1, 0, 1) -- 1 soniya TTL
    if count and count > 20 then
        ngx.log(ngx.WARN, "WebSocket Flood aniqlandi! Ulanish to'xtatildi: ", client_ip)
        wb:send_close(1008, "Tezlik chegarasidan oshildi (Policy Violation)")
        return false
    end
    return true
end""",
        "expl": "WebSocket ochilgach Nginx ning odatiy HTTP rate-limiting modullari ishlamay qoladi, chunki barcha amallar bitta TCP sessiyasi ichida o'tadi. Shuning uchun freymlar qabul qilinayotgan siklda qat'iy mantiqiy cheklov o'rnatish tizim xavfsizligining garovidir."
    },
    {
        "id": 1148,
        "title": "Real-time fond birjasi kotirovkalarini WebSocket orqali minglab mijozlarga tarqatuvchi broker",
        "desc": "Bitta birja narxi o'zgarganda (masalan TSLA aksiyasi narxi), bir vaqtning o'zida serverga ulangan 50 000 ta treyderga ushbu yangilikni minimal kechikish bilan yetkazish kerak.",
        "req": "Mahalliy worker ichida ulanishlar ro'yxatini saqlash, xabar kelganda massiv bo'yicha tezkor iteratsiya qilib `wb:send_text()` chaqirish.",
        "code": """-- Mahalliy Worker darajasida xabarlarni keng tarqatuvchi (Broadcaster)
local _M = {}
local local_connections = {}

function _M.add_client(client_id, wb)
    local_connections[client_id] = wb
end

function _M.remove_client(client_id)
    local_connections[client_id] = nil
end

function _M.broadcast_quote(symbol, price)
    local payload = string.format('{"symbol":"%s","price":%.2f}', symbol, price)
    
    for id, wb in pairs(local_connections) do
        local ok, err = wb:send_text(payload)
        if not ok then
            -- Ulanish uzilgan bo'lsa tozalash
            local_connections[id] = nil
        end
    end
end

return _M""",
        "expl": "Har bir Nginx workeri o'zining mahalliy Lua jadvalida faqat o'ziga ulangan mijozlarni saqlaydi. Broadkasting paytida hech qanday qulflar (locks) yoki resurs raqobati yuzaga kelmaydi, bu esa soniyasiga yuz minglab xabarlarni tarqatish unumdorligini ta'minlaydi."
    },
    {
        "id": 1149,
        "title": "WebSocket ulanishini xavfsiz va namunali yopish (RFC 6455 standartidagi close kodlari: 1000, 1001)",
        "desc": "Ulanishni shunchaki TCP darajasida uzib yuborish mijoz tomonida (brauzerda) xatolik keltirib chiqaradi. Protokol bo'yicha ikki tomonlama Close Handshake o'tkazilishi shart.",
        "req": "RFC 6455 standart kodlaridan (1000 Normal, 1001 Going Away, 1008 Policy Violation) to'g'ri foydalanish, yopilish javobini kutish.",
        "code": """-- Namunali WebSocket Close Handshake
local function graceful_websocket_close(wb, status_code, reason)
    status_code = status_code or 1000
    reason = reason or "Normal Shutdown"
    
    -- 1. Mijozga Close freymini yuborish
    local bytes, err = wb:send_close(status_code, reason)
    if not bytes then
        ngx.log(ngx.ERR, "Close freymini yuborishda xato: ", err)
        return
    end
    
    -- 2. Mijozdan javobiy Close freymini kutish (maksimal 1 soniya)
    wb:set_timeout(1000)
    while true do
        local data, typ, recv_err = wb:recv_frame()
        if not data or typ == "close" then
            break -- Yopilish muvaffaqiyatli yakunlandi
        end
    end
    
    ngx.log(ngx.INFO, "WebSocket sessiyasi namunali yakunlandi")
end""",
        "expl": "RFC 6455 bo'yicha tomonlardan biri 'Close Frame' yuborganida, ikkinchi tomon ham javoban 'Close Frame' yuborishi shart. Shundan keyingina TCP soketi yopiladi. Bu holat mijoz ilovasiga qayta ulanish (reconnect) kerakmi yoki yo'qligini to'g'ri tushunish imkonini beradi."
    },
    {
        "id": 1150,
        "title": "WebSocket orqali ikki tomonlama RPC (Remote Procedure Call) tizimi va asinxron javob kutish",
        "desc": "Mijoz WebSocket orqali so'rov yuboradi (`{id: 42, method: 'getUser', params: {...}}`) va aynan shu so'rovga serverdan asinxron javob kutadi.",
        "req": "JSON-RPC 2.0 formatini qo'llash, requestId bo'yicha javoblarni korrelyatsiya qilish, xatoliklarni standart formatda qaytarish.",
        "code": """-- WebSocket orqali JSON-RPC 2.0 Shlyuzi
local cjson = require "cjson.safe"
local _M = {}

local methods = {
    ["ping"] = function(params) return "pong" end,
    ["calculate_tax"] = function(params) return (params.amount or 0) * 0.12 end
}

function _M.handle_rpc_message(wb, raw_json)
    local req = cjson.decode(raw_json)
    if not req or not req.id or not req.method then
        wb:send_text('{"jsonrpc":"2.0","error":{"code":-32600,"message":"Invalid Request"}}')
        return
    end
    
    local handler = methods[req.method]
    if not handler then
        local err_resp = {
            jsonrpc = "2.0",
            id = req.id,
            error = { code = -32601, message = "Method not found" }
        }
        wb:send_text(cjson.encode(err_resp))
        return
    end
    
    local ok, result = pcall(handler, req.params or {})
    local resp = {
        jsonrpc = "2.0",
        id = req.id,
        result = ok and result or nil,
        error = not ok and { code = -32000, message = tostring(result) } or nil
    }
    
    wb:send_text(cjson.encode(resp))
end

return _M""",
        "expl": "WebSocket orqali RPC arxitekturasi HTTP so'rovlariga nisbatan har bir operatsiyada 1-2 ms vaqtni tejaydi, chunki yangi TCP/TLS ulanishi ochilmaydi va HTTP sarlavhalari takroran uzatilmaydi. Barcha amallar yagona doimiy kanal orqali asinxron marshrutlanadi."
    }
]
