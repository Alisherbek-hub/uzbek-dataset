# -*- coding: utf-8 -*-
"""
Lua 23-modul: 1101 dan 1125 gacha bo'lgan topshiriqlar
OpenResty cosocket API, TCP/UDP oqimlari, Nginx Stream proksi va Redis
"""

TASKS_1101_1125 = [
    {
        "id": 1101,
        "title": "ngx.socket.tcp() bilan asosiy TCP klient va timeoutlarni boshqarish",
        "desc": "OpenResty ilovasida tashqi TCP xizmatiga ulanish, so'rov yuborish va javobni to'liq qabul qilish talab etiladi. Nginx worker jarayoni biron bir holatda bloklanib qolmasligi shart.",
        "req": "`ngx.socket.tcp()` dan foydalanish, ulanish, o'qish va yozish timeoutlarini alohida sozlash, `receive('*l')` orqali satr o'qish va xatoliklarni xavfsiz qayta ishlash.",
        "code": """-- OpenResty da noblokirovka qiluvchi TCP mijozi
local _M = {}

function _M.query_tcp_service(host, port, payload)
    local tcp = ngx.socket.tcp()
    
    -- Timeout parametrlarini sozlash: ulanish, o'qish, yozish (millisekundlarda)
    tcp:settimeouts(2000, 5000, 5000)
    
    -- Tashqi server bilan ulanish o'rnatish
    local ok, err = tcp:connect(host, port)
    if not ok then
        return nil, "Ulanish xatosi: " .. tostring(err)
    end
    
    -- Ma'lumotlarni yuborish
    local bytes_sent, send_err = tcp:send(payload .. "\\r\\n")
    if not bytes_sent then
        tcp:close()
        return nil, "Ma'lumot yuborish xatosi: " .. tostring(send_err)
    end
    
    -- Javobni bitta qator shaklida o'qish ('*l' parametri)
    local line, read_err = tcp:receive("*l")
    if not line then
        tcp:close()
        return nil, "O'qish xatosi: " .. tostring(read_err)
    end
    
    -- Ulanishni yopish
    tcp:close()
    return line, nil
end

return _M""",
        "expl": "OpenResty Cosocket API Nginx event loop (epoll/kqueue) ustiga qurilgan. `tcp:connect()` va `tcp:receive()` chaqirilganda, Lua korutinasi (coroutine) orqaga chekinadi (yield) va OS hodisasi yuz berganda avtomatik qayta uyg'onadi (resume). Bu bitta workerda o'n minglab parallel TCP ulanishlarni CPU va xotirani band qilmasdan bajarish imkonini beradi."
    },
    {
        "id": 1102,
        "title": "TCP Cosocket ulanishlar hovuzi (setkeepalive max_idle_timeout va pool_size)",
        "desc": "Har bir so'rov uchun yangidan TCP ulanish ochish va 3 bosqichli handshake (SYN, SYN-ACK, ACK) bajarish server protsessoriga va tarmoqqa ortiqcha yuklama keltiradi.",
        "req": "`sock:setkeepalive(timeout, size)` metodidan foydalanish, ulanishni yopmasdan hovuzga qaytarish, hovuz to'lganida xavfsiz yopish.",
        "code": """-- Ulanishlar hovuzi (Keepalive Connection Pool) boshqaruvi
local _M = {}

local DEFAULT_IDLE_TIMEOUT = 10000 -- 10 soniya kutish
local DEFAULT_POOL_SIZE = 100      -- Hovuzdagi maksimal ochiq soketlar soni

function _M.execute_with_keepalive(host, port, request_data)
    local sock = ngx.socket.tcp()
    sock:settimeouts(1000, 3000, 3000)
    
    local ok, err = sock:connect(host, port)
    if not ok then
        return nil, "Ulanish muvaffaqiyatsiz: " .. tostring(err)
    end
    
    local _, send_err = sock:send(request_data)
    if send_err then
        sock:close()
        return nil, send_err
    end
    
    local response, recv_err = sock:receive("*l")
    if not response then
        sock:close()
        return nil, recv_err
    end
    
    -- Ulanishni yopish o'rniga uni hovuzga qaytaramiz
    local keepalive_ok, keepalive_err = sock:setkeepalive(DEFAULT_IDLE_TIMEOUT, DEFAULT_POOL_SIZE)
    if not keepalive_ok then
        ngx.log(ngx.WARN, "Hovuzga qaytarish xatosi (yopilmoqda): ", keepalive_err)
        sock:close()
    end
    
    return response, nil
end

return _M""",
        "expl": "`sock:setkeepalive()` chaqirilganda, OpenResty joriy Nginx worker doirasida host va port kombinatsiyasi bo'yicha ulanishni maxsus ro'yxatda saqlaydi. Keyingi `sock:connect()` chaqirilganida, agar bo'sh soket mavjud bo'lsa, tarmoq darajasidagi handshake'larsiz darhol o'sha soket qayta ishlatiladi. Bu kechikishni (latency) 80% gacha kamaytiradi."
    },
    {
        "id": 1103,
        "title": "sock:sslhandshake orqali xavfsiz TLS/SSL aloqasini o'rnatish va SNI tekshiruvi",
        "desc": "Tashqi HTTPS yoki maxsus shifrlangan TCP protokollariga ulanishda shifrlash kalitlarini almashish va serverning haqiqiy domeniga tegishli ekanligini (SNI) tekshirish zarur.",
        "req": "`sock:sslhandshake(reused_session, server_name, ssl_verify)` dan foydalanish, sessiyani keshlashtirish va xavfsiz TLS o'rnatish.",
        "code": """-- TLS Handshake va SNI tekshiruvi
local _M = {}

function _M.connect_secure_tls(host, port)
    local sock = ngx.socket.tcp()
    sock:settimeouts(2000, 5000, 5000)
    
    local ok, err = sock:connect(host, port)
    if not ok then
        return nil, "TCP ulanish xatosi: " .. tostring(err)
    end
    
    -- TLS Handshake o'tkazish
    -- Parametrlar: session (nil = yangi), server_name (SNI), ssl_verify (true = sertifikat tekshiruvi)
    local session, ssl_err = sock:sslhandshake(nil, host, true)
    if not session and ssl_err then
        sock:close()
        return nil, "TLS Handshake xatosi: " .. tostring(ssl_err)
    end
    
    ngx.log(ngx.INFO, "Xavfsiz TLS aloqasi muvaffaqiyatli o'rnatildi: ", host)
    return sock, nil
end

return _M""",
        "expl": "OpenResty ning `sslhandshake()` metodi OpenSSL non-blocking API lari bilan birlashtirilgan. `server_name` parametri zamonaviy bulutli servislarda (Cloudflare, AWS) bitta IP manzilida yuzlab turli domenlar joylashganda to'g'ri sertifikatni tanlash (SNI) uchun qat'iy talab etiladi."
    },
    {
        "id": 1104,
        "title": "Asinxron TCP Echo server va mijoz aloqasi protokoli",
        "desc": "Tarmoq uskunalarini sinovdan o'tkazish va aloqa kanalining kechikishini doimiy baholash uchun yuqori unumdor TCP Echo protokoli kerak.",
        "req": "TCP ulanishida belgilangan hajmda ma'lumot qabul qilish (`receive(n)`), qabul qilingan ma'lumotni o'zgarishsiz qaytarish va xotira oqishini oldini olish.",
        "code": """-- TCP Echo xizmati mantiqi
local _M = {}

function _M.handle_echo_session(client_sock)
    client_sock:settimeouts(5000, 5000, 5000)
    
    while true do
        -- 1024 baytlik paketni kutish
        local data, err, partial = client_sock:receive(1024)
        if not data then
            if err == "closed" then
                ngx.log(ngx.INFO, "Mijoz ulanishni yopdi")
                break
            end
            ngx.log(ngx.ERR, "Qabul qilishda xato: ", err)
            break
        end
        
        -- Kelgan ma'lumotni darhol orqaga qaytarish
        local bytes, send_err = client_sock:send(data)
        if not bytes then
            ngx.log(ngx.ERR, "Qaytarishda xatolik: ", send_err)
            break
        end
    end
    
    client_sock:close()
end

return _M""",
        "expl": "`receive(n)` parametri aniq $n$ bayt yetib kelguncha kutadi. Bu binar protokollarda aniq belgilangan kadrlar (frames) bilan ishlashda qulaydir. `err == 'closed'` tekshiruvi mijoz tomonidan ulanish normal uzilganini ifodalaydi."
    },
    {
        "id": 1105,
        "title": "Maxsus binar protokollarni paketlash va parslash (Binar header + payload)",
        "desc": "Moliyaviy va telemetriya tizimlarida ma'lumotlar JSON o'rniga binar formatda uzatiladi: 2 bayt Sehrli raqam (Magic), 2 bayt Buyruq kodi (Command), 4 bayt Ma'lumot uzunligi (Length), va Payload.",
        "req": "String pack/unpack funksiyalaridan foydalanish, binar sarlavhani ajratish, payloadni to'liq o'qish.",
        "code": """-- Binar protokollarni enkoder va dekoderi
local _M = {}

local MAGIC_NUMBER = 0xABCD

--- Paketni tuzish: >I2 (magic) >I2 (cmd) >I4 (length) + payload
function _M.encode_packet(command_id, payload)
    local payload_len = #payload
    -- Big-endian formatida binar qadoqlash
    local header = string.pack(">I2I2I4", MAGIC_NUMBER, command_id, payload_len)
    return header .. payload
end

--- Soketdan paketni ajratib olish
function _M.read_packet(sock)
    -- 1. Avval 8 baytlik sarlavhani o'qish
    local header_data, err = sock:receive(8)
    if not header_data then
        return nil, nil, "Sarlavhani o'qishda xato: " .. tostring(err)
    end
    
    local magic, cmd, length = string.unpack(">I2I2I4", header_data)
    if magic ~= MAGIC_NUMBER then
        return nil, nil, "Noto'g'ri protokol magic raqami"
    end
    
    -- 2. Ko'rsatilgan uzunlikdagi haqiqiy ma'lumotni o'qish
    local payload, payload_err = sock:receive(length)
    if not payload then
        return nil, nil, "Payload o'qishda xato: " .. tostring(payload_err)
    end
    
    return cmd, payload, nil
end

return _M""",
        "expl": "Lua 5.3 va LuaJIT 2.1 da `string.pack` va `string.unpack` yordamida binar oqimlar C tili tezligida tahlil qilinadi. Big-endian `>I2I2I4` formati tarmoq baytlar tartibiga (Network Byte Order) to'liq mos keladi va JSON parslariga nisbatan 10-15 barobar kamroq CPU resursini talab qiladi."
    },
    {
        "id": 1106,
        "title": "Cosocket xatoliklarini boshqarish va eksponentsial kechikish bilan qayta urinish (Retry with Exponential Backoff)",
        "desc": "Tashqi mikroxizmatlar vaqtincha javob bermay qolishi mumkin. Ulanishni birdaniga to'xtatmasdan, oqilona kechikishlar bilan qayta urinish (retry) lozim.",
        "req": "Maksimal urinishlar soni (3 marta), `ngx.sleep` yordamida noblokirovka qiluvchi kechikish, eksponentsial ko'payish va jitter qo'shish.",
        "code": """-- Eksponentsial kechikishli qayta urinish mexanizmi
local _M = {}

function _M.reliable_connect(host, port, max_retries)
    max_retries = max_retries or 3
    local delay = 0.1 -- 100ms boshlang'ich kechikish
    
    for attempt = 1, max_retries do
        local sock = ngx.socket.tcp()
        sock:settimeouts(1000, 2000, 2000)
        
        local ok, err = sock:connect(host, port)
        if ok then
            return sock, nil
        end
        
        ngx.log(ngx.WARN, string.format("Ulanish urinishi %d muvaffaqiyatsiz: %s", attempt, err))
        
        if attempt < max_retries then
            -- Jitter qo'shilgan noblokirovka qiluvchi pauza
            local jitter = math.random() * 0.05
            ngx.sleep(delay + jitter)
            delay = delay * 2 -- Eksponentsial oshirish
        end
    end
    
    return nil, "Barcha qayta urinishlar muvaffaqiyatsiz yakunlandi"
end

return _M""",
        "expl": "`ngx.sleep()` Nginx hodisalar mexanizmida taymer yaratadi va operatsion tizim `sleep` funksiyasidan farqli ravishda worker jarayonini mutlaqo to'xtatib qo'ymaydi. Jitter qo'shilishi esa serverga minglab klientlarning bir vaqtda to'lqin bo'lib urilishining (Thundering Herd) oldini oladi."
    },
    {
        "id": 1107,
        "title": "resty.dns.resolver orqali asinxron DNS so'rovlari va A/AAAA yozuvlarini aniqlash",
        "desc": "Standart C kutubxonasidagi `gethostbyname` Nginx worker jarayonini to'liq bloklab qo'yadi. Shu sababli domen nomlarini IP manzilga o'girish to'liq asinxron DNS resolver orqali bajarilishi shart.",
        "req": "`resty.dns.resolver` dan foydalanish, 8.8.8.8 serveriga ulanish, A va AAAA yozuvlarini so'rash, kesh muddati (TTL) ni hisobga olish.",
        "code": """-- Asinxron DNS yechuvchi
local resolver = require "resty.dns.resolver"
local _M = {}

function _M.resolve_domain(domain_name)
    local r, err = resolver:new{
        nameservers = {"8.8.8.8", "1.1.1.1"},
        retrans = 2,  -- 2 marta qayta yuborish
        timeout = 2000, -- 2 soniya timeout
    }
    if not r then
        return nil, "Resolver yaratishda xato: " .. tostring(err)
    end
    
    -- IPv4 A yozuvlarini so'rash
    local answers, query_err = r:query(domain_name, { qtype = r.TYPE_A })
    if not answers then
        return nil, "DNS so'rov xatosi: " .. tostring(query_err)
    end
    
    if answers.errcode then
        return nil, "DNS server xatosi kodi: " .. answers.errcode .. ": " .. answers.errstr
    end
    
    local ip_list = {}
    for _, ans in ipairs(answers) do
        if ans.address then
            table.insert(ip_list, { ip = ans.address, ttl = ans.ttl })
        end
    end
    
    return ip_list, nil
end

return _M""",
        "expl": "`resty.dns.resolver` sof Lua va cosocket UDP asosida yozilgan bo'lib, DNS so'rovlarini 100% noblokirovka rejimida bajaradi. Tizim DNS yozuvlarining `ttl` qiymatini oladi, bu esa dasturchiga Nginx umumiy xotirasida (`lua_shared_dict`) mahalliy kesh yaratish imkonini beradi."
    },
    {
        "id": 1108,
        "title": "Katta hajmdagi TCP oqimini buferga yig'masdan qismlab (chunked streaming) uzatish",
        "desc": "Katta hajmdagi ma'lumotlarni (masalan, 500 MB loglar yoki audio oqimlar) uzatishda barcha baytlarni Lua satriga yig'ish xotira tugashiga (OOM) olib keladi.",
        "req": "Oqimli o'qish va yozish siklini qurish, `receive(chunk_size)` orqali bo'laklab olish, `send()` orqali mijozga darhol yetkazish va xotira nazorati.",
        "code": """-- Xotira tejamkor oqimli uzatgich (Chunked Stream Pipe)
local _M = {}

local CHUNK_SIZE = 64 * 1024 -- 64 KB qismlar

function _M.pipe_stream(source_sock, dest_sock)
    local total_bytes = 0
    
    while true do
        -- Manbadan 64KB o'qish
        local chunk, err, partial = source_sock:receive(CHUNK_SIZE)
        local data_to_send = chunk or partial
        
        if data_to_send and #data_to_send > 0 then
            local bytes_sent, send_err = dest_sock:send(data_to_send)
            if not bytes_sent then
                return total_bytes, "Maqsadga yozishda xato: " .. tostring(send_err)
            end
            total_bytes = total_bytes + bytes_sent
        end
        
        if err then
            if err == "closed" then
                -- Oqim muvaffaqiyatli yakunlandi
                break
            else
                return total_bytes, "O'qishda xatolik yuz berdi: " .. tostring(err)
            end
        end
    end
    
    return total_bytes, nil
end

return _M""",
        "expl": "Ushbu yechim xotira sarfini qat'iy 64 KB miqdorida ushlab turadi. Qancha gigabayt ma'lumot o'tishidan qat'i nazar, LuaJIT xotira axlat yig'uvchisiga (GC) bosim tushmaydi. `partial` parametri esa ulanish yopilayotgan paytda oxirgi baytlar yo'qolishining oldini oladi."
    },
    {
        "id": 1109,
        "title": "OpenResty ngx.timer.at orqali fonda ishlovchi TCP sog'liq tekshiruvchisi (Health Checker)",
        "desc": "Yuklama taqsimlovchi (Upstream Load Balancer) orqa fondagi backend serverlarning ishchi holatini mijoz so'rovlariga xalaqit bermasdan davriy tekshirib turishi kerak.",
        "req": "`ngx.timer.at` rekursiv chaqiruvi, worker 0 orqali tekshirish (dublikatsiyani oldini olish), `lua_shared_dict` ga sog'lomlik maqomini yozish.",
        "code": """-- Orqa fonda ishlovchi Health Checker
local _M = {}
local CHECK_INTERVAL = 5 -- Har 5 soniyada

local function check_peer(premature, host, port)
    if premature then return end -- Worker to'xtatilayotgan bo'lsa
    
    local sock = ngx.socket.tcp()
    sock:settimeout(1000)
    local ok, err = sock:connect(host, port)
    
    local shared_status = ngx.shared.health_status
    if ok then
        shared_status:set(host .. ":" .. port, true)
        sock:close()
    else
        shared_status:set(host .. ":" .. port, false)
        ngx.log(ngx.WARN, "Backend ishlamayapti: ", host, ":", port, " Xato: ", err)
    end
    
    -- Keyingi tekshiruvni rejalashtirish
    local ok_timer, timer_err = ngx.timer.at(CHECK_INTERVAL, check_peer, host, port)
    if not ok_timer then
        ngx.log(ngx.ERR, "Taymer yaratish xatosi: ", timer_err)
    end
end

function _M.spawn_checker(host, port)
    -- Faqat 0-raqamli worker tekshiruv o'tkazadi
    if ngx.worker.id() == 0 then
        ngx.timer.at(0, check_peer, host, port)
    end
end

return _M""",
        "expl": "OpenResty `ngx.timer.at` Nginx worker jarayonining fonida ishlovchi 'yengil iplar' (light threads) yaratadi. `ngx.worker.id() == 0` filtri orqali serverda 16 ta worker bo'lsa ham, tekshiruv faqat 1 ta worker tomonidan qilinadi, bu esa backendga ortiqcha so'rovlar yog'ilishini bartaraf qiladi."
    },
    {
        "id": 1110,
        "title": "Cosocket orqali SMTP serverga ulanib elektron xat (email) jo'natish mantiqi",
        "desc": "Tizim ma'murlariga xavfsizlik hodisalari va kritik avariyalar haqida darhol ogohlantiruvchi elektron pochta xabarlarini to'g'ridan-to'g'ri Nginx dan jo'natish zarur.",
        "req": "SMTP protokolining asosiy buyruqlarini (HELO, MAIL FROM, RCPT TO, DATA, QUIT) ketma-ket bajarish, server javob kodlarini (220, 250, 354) tekshirish.",
        "code": """-- Cosocket orqali SMTP xat yuboruvchi
local _M = {}

local function send_smtp_cmd(sock, cmd, expected_code)
    local _, err = sock:send(cmd .. "\\r\\n")
    if err then return false, err end
    
    local line, read_err = sock:receive("*l")
    if not line then return false, read_err end
    
    local code = tonumber(string.sub(line, 1, 3))
    if code ~= expected_code then
        return false, "Kutilmagan SMTP javobi: " .. line
    end
    return true, nil
end

function _M.send_email(smtp_host, smtp_port, from_addr, to_addr, subject, body)
    local sock = ngx.socket.tcp()
    sock:settimeouts(2000, 5000, 5000)
    
    local ok, err = sock:connect(smtp_host, smtp_port)
    if not ok then return false, "SMTP ulanish xatosi: " .. tostring(err) end
    
    -- Banner (220) o'qish
    local banner = sock:receive("*l")
    
    local steps = {
        {"HELO openresty.local", 250},
        {"MAIL FROM:<" .. from_addr .. ">", 250},
        {"RCPT TO:<" .. to_addr .. ">", 250},
        {"DATA", 354}
    }
    
    for _, step in ipairs(steps) do
        local success, step_err = send_smtp_cmd(sock, step[1], step[2])
        if not success then
            sock:close()
            return false, step_err
        end
    end
    
    -- Xat tanasini yuborish
    local email_content = "Subject: " .. subject .. "\\r\\n\\r\\n" .. body .. "\\r\\n.\\r\\n"
    local _, data_err = sock:send(email_content)
    if data_err then
        sock:close()
        return false, data_err
    end
    
    send_smtp_cmd(sock, "QUIT", 221)
    sock:close()
    return true, nil
end

return _M""",
        "expl": "OpenResty yordamida har qanday amaliy tarmoq protokoli (SMTP, FTP, POP3) sof Lua tilida bir necha o'n qatorda amalga oshirilishi mumkin. Ulanish asinxron bo'lgani sababli, xat yuborilayotgan paytda Nginx boshqa minglab HTTP foydalanuvchilariga xizmat ko'rsatishda davom etadi."
    },
    {
        "id": 1111,
        "title": "Nginx Stream kontekstida preread_by_lua_block: TLS ClientHello orqali SNI aniqlash va dinamik marshrutlash",
        "desc": "TCP darajasidagi Nginx proksi serverida TLS trafigini dekodlamasdan (shifrlangan holda), mijoz murojaat qilayotgan domen nomini (SNI) aniqlash va shunga mos backend serverga yo'naltirish zarur.",
        "req": "`ngx.req.socket(true)` orqali preread soketini olish, TLS ClientHello paketini parslash, `ngx.var.upstream_target` o'zgaruvchisini o'rnatish.",
        "code": """-- nginx.conf stream ichida preread_by_lua_block
-- TLS ClientHello paketidan Server Name Indication (SNI) ni ajratish
local function extract_sni()
    local sock = ngx.req.socket(true) -- Peeking socket (oqimni buzmaydi)
    
    -- Record Header: 5 bayt (Type 1, Version 2, Length 2)
    local header, err = sock:receive(5)
    if not header then return nil end
    
    local content_type, _, length = string.unpack(">I1I2I2", header)
    if content_type ~= 22 then -- 22 = Handshake
        return nil
    end
    
    local handshake_data = sock:receive(length)
    if not handshake_data then return nil end
    
    -- Oddiy SNI qidirish (TLS kengaytmasi bo'yicha)
    local sni = string.match(handshake_data, "([%a%d%.-]+%.[a-z]{2,})")
    return sni
end

local sni = extract_sni()
if sni == "api.production.uz" then
    ngx.var.target_backend = "10.0.1.10:443"
elseif sni == "secure.payments.uz" then
    ngx.var.target_backend = "10.0.2.20:443"
else
    ngx.var.target_backend = "10.0.0.1:443"
end""",
        "expl": "`preread_by_lua_block` Nginx Stream moduli ulanishni qabul qilgan, biroq backendga yo'naltirmagan vaqtda ishlaydi. `ngx.req.socket(true)` orqali olingan soketdagi ma'lumotlar o'qilsa ham buferda saqlanib qoladi (peeking). Natijada TLS shifrlash kalitlarini bermasdan domenlar bo'yicha marshrutlash imkoni yaratiladi."
    },
    {
        "id": 1112,
        "title": "Nginx Stream kontekstida content_by_lua_block: Maxsus TCP shlyuz proksi (Custom Gateway)",
        "desc": "TCP paketlarini shunchaki yo'naltirmasdan, ularni shifrlash, filtrdan o'tkazish yoki audit qilish uchun to'liq Lua nazoratidagi TCP proksi shlyuzi yaratilishi lozim.",
        "req": "Mijoz va Backend o'rtasida ikki tomonlama dupleks korutina orqali baytlarni uzatish (`ngx.thread.spawn`), ulanishlarni o'z vaqtida tozalash.",
        "code": """-- Stream content_by_lua_block da to'liq dupleks TCP shlyuzi
local client_sock = ngx.req.socket()
local backend_sock = ngx.socket.tcp()

backend_sock:settimeouts(5000, 5000, 5000)
local ok, err = backend_sock:connect("127.0.0.1", 9000)
if not ok then
    ngx.log(ngx.ERR, "Backendga ulanib bo'lmadi: ", err)
    return ngx.exit(ngx.ERROR)
end

-- 1-Yo'nalish: Mijozdan Backendga ma'lumot uzatuvchi fon iplari
local function forward(src, dst, label)
    while true do
        local data, recv_err, partial = src:receive(8192)
        local payload = data or partial
        if payload and #payload > 0 then
            local _, send_err = dst:send(payload)
            if send_err then break end
        end
        if recv_err then break end
    end
    dst:close()
end

local t1 = ngx.thread.spawn(forward, client_sock, backend_sock, "C->B")
local t2 = ngx.thread.spawn(forward, backend_sock, client_sock, "B->C")

ngx.thread.wait(t1, t2)""",
        "expl": "`ngx.thread.spawn` yordamida Nginx ichida bitta TCP sessiyasi uchun ikkita parallel 'Light Thread' ochiladi. Biri mijozdan kelgan paketlarni backendga oqizadi, ikkinchisi backend javobini mijozga qaytaradi. `ngx.thread.wait` ikkala yo'nalish yakunlanguncha kutadi."
    },
    {
        "id": 1113,
        "title": "ngx.socket.udp() orqali asinxron Syslog yozuvlarini markaziy serverga yuborish",
        "desc": "Kritik xavfsizlik audit loglarini (RFC 5424 standarti) diskka yozib I/O qotishini kutmasdan, UDP orqali zudlik bilan markaziy SIEM / Syslog serveriga jo'natish kerak.",
        "req": "`ngx.socket.udp()` dan foydalanish, Syslog PRI (Facility + Severity) sarlavhasini shakllantirish, paketni yo'qotmasdan yuborish.",
        "code": """-- Asinxron UDP Syslog jo'natuvchi
local _M = {}

local FACILITY_LOCAL0 = 16
local SEVERITY_WARNING = 4

function _M.send_syslog(server_host, server_port, app_name, message)
    local udp = ngx.socket.udp()
    local ok, err = udp:setpeername(server_host, server_port)
    if not ok then
        return nil, "UDP ulanish xatosi: " .. tostring(err)
    end
    
    -- PRI qiymatini hisoblash: Facility * 8 + Severity
    local pri = FACILITY_LOCAL0 * 8 + SEVERITY_WARNING
    local timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
    
    -- RFC 5424 formati: <PRI>VERSION TIMESTAMP HOSTNAME APPNAME PROCID MSGID MSG
    local syslog_msg = string.format("<%d>1 %s openresty %s - - - %s", pri, timestamp, app_name, message)
    
    local sent_ok, send_err = udp:send(syslog_msg)
    udp:close()
    
    if not sent_ok then
        return nil, "Yuborish xatosi: " .. tostring(send_err)
    end
    return true, nil
end

return _M""",
        "expl": "UDP soketlarida `setpeername` operatsion tizim darajasida IP marshrutini belgilaydi, lekin hech qanday tarmoq handshakelarini amalga oshirmaydi. `udp:send()` chaqiruvi mikrosekundlarda bajariladi va web-server unumdorligiga nol ta'sir ko'rsatgan holda audit yozuvlarini uzatadi."
    },
    {
        "id": 1114,
        "title": "UDP orqali StatsD / Prometheus metrikalarini (Counter/Gauge) yuboruvchi agent",
        "desc": "Har bir kiruvchi so'rovning davomiyligi, HTTP holat kodlari va xotira holatini monitoring tizimiga (StatsD / Datadog) yuboruvchi yengil agent talab qilinadi.",
        "req": "StatsD protokoli sintaksisi (`metric:value|c` yoki `metric:value|ms`), paketlarni birlashtirish (batching) va UDP orqali uzatish.",
        "code": """-- StatsD metrika to'plovchisi
local _M = {}

local udp_socket = nil

function _M.init(host, port)
    local sock = ngx.socket.udp()
    local ok, err = sock:setpeername(host, port)
    if not ok then
        ngx.log(ngx.ERR, "StatsD ulanish xatosi: ", err)
        return false
    end
    udp_socket = sock
    return true
end

function _M.increment(metric, value)
    if not udp_socket then return end
    value = value or 1
    local payload = string.format("%s:%d|c", metric, value)
    udp_socket:send(payload)
end

function _M.timing(metric, milliseconds)
    if not udp_socket then return end
    local payload = string.format("%s:%d|ms", metric, milliseconds)
    udp_socket:send(payload)
end

return _M""",
        "expl": "StatsD orqali metrikalarni 'Fire-and-Forget' (yubor va unut) rejimida uzatish production tizimlarida qat'iy standartdir. Agar monitoring serveri ishlamay qolsa ham, UDP ulanishsiz bo'lgani sababli OpenResty mijozlarga hech qanday xatosiz xizmat ko'rsatishda davom etadi."
    },
    {
        "id": 1115,
        "title": "Nginx Stream da dinamik og'irlik asosidagi (Weighted Round Robin) TCP yuklama taqsimlovchi",
        "desc": "Turli quvvatdagi backend serverlariga (masalan, server A = 70% yuklama, server B = 30%) kiruvchi TCP ulanishlarini mos proporsiyada taqsimlash kerak.",
        "req": "Weighted Round Robin algoritmini implementatsiya qilish, backend serverlar ro'yxatini va og'irliklarini saqlash, navbatdagi tanlangan IP ni qaytarish.",
        "code": """-- Weighted Round Robin TCP Balancer
local _M = {}

local backends = {
    { addr = "192.168.1.10:3306", weight = 7, current_weight = 0 },
    { addr = "192.168.1.11:3306", weight = 3, current_weight = 0 }
}

function _M.get_next_peer()
    local total_weight = 0
    local best = nil
    
    for _, peer in ipairs(backends) do
        peer.current_weight = peer.current_weight + peer.weight
        total_weight = total_weight + peer.weight
        
        if not best or peer.current_weight > best.current_weight then
            best = peer
        end
    end
    
    if not best then return nil end
    best.current_weight = best.current_weight - total_weight
    return best.addr
end

return _M""",
        "expl": "Smooth Weighted Round-Robin (Nginx ning o'rnatilgan algoritmi) har bir tanlovda serverlarning `current_weight` qiymatini o'zgartirib boradi. Bu ketma-ket bitta kuchli serverga 7 ta ulanish tushib ketmasdan, 7:3 nisbatida ulanishlar juda silliq (interleaved) taqsimlanishini kafolatlaydi."
    },
    {
        "id": 1116,
        "title": "Nginx Stream darajasida lua_shared_dict yordamida IP bo'yicha ulanishlar soni va tezligini cheklash (Rate Limiter)",
        "desc": "TCP portlariga (masalan, SSH yoki DB porti) qilinadigan DDoS va Brute-Force hujumlarini Nginx Stream qatlamining o'zidayoq ushlab, bloklash lozim.",
        "req": "`lua_shared_dict` xotirasidan foydalanish, sekundiga maksimal 10 ta ulanish chegarasi, chegaradan oshsa ulanishni darhol uzish.",
        "code": """-- Stream darajasida IP Rate Limiter
local limit_dict = ngx.shared.stream_rate_limit
local client_ip = ngx.var.remote_addr
local limit_per_sec = 10

local key = "rate:" .. client_ip
local current, err = limit_dict:incr(key, 1, 0, 1) -- 1 soniya TTL bilan

if current and current > limit_per_sec then
    ngx.log(ngx.WARN, "DDoS himoyasi ishga tushdi, IP bloklandi: ", client_ip)
    return ngx.exit(ngx.ERROR) -- Ulanishni darhol uzish
end""",
        "expl": "Stream darajasidagi rate-limiting eng erta bosqichda ishlaydi. Hujumchi hali TLS yoki ma'lumotlar almashish bosqichiga yetmasidanoq, Nginx darajasida TCP FIN/RST orqali uziladi, bu esa orqa fondagi bazalar va autentifikatsiya serverlarini ortiqcha hisoblashlardan to'liq asraydi."
    },
    {
        "id": 1117,
        "title": "Stream orqali MySQL ulanish handshakeni ushlash va kiruvchi so'rovlarni xavfsizlik audit logiga yozish",
        "desc": "Tashkilot xavfsizligi talablariga ko'ra, ma'lumotlar bazasiga kim, qaysi IP dan va qaysi foydalanuvchi nomi bilan ulanayotganini Nginx shlyuzida ushlab, audit logiga yozish kerak.",
        "req": "MySQL Server Greeting va Client Authentication paketlarini parslash, foydalanuvchi nomini ajratish va logga yozish.",
        "code": """-- MySQL handshake audit mantiqi
local sock = ngx.req.socket()

-- MySQL Initial Handshake Packet (Server Greeting)
-- Birinchi 4 bayt: 3 bayt paket uzunligi + 1 bayt sequence
local p_header, err = sock:receive(4)
if p_header then
    local p_len = string.byte(p_header, 1) + string.byte(p_header, 2) * 256
    local payload = sock:receive(p_len)
    
    -- Server versiyasi va server imkoniyatlari
    local proto_version = string.byte(payload, 1)
    ngx.log(ngx.INFO, "MySQL Server Protokol versiyasi: ", proto_version)
end""",
        "expl": "MySQL protokoli holatga ega (stateful) binar protokoldir. Nginx Stream orqali o'tayotgan paketlarni tahlil qilish orqali shaffof ma'lumotlar bazasi xavfsizlik devori (Database Firewall / WAF) yaratish mumkin bo'ladi."
    },
    {
        "id": 1118,
        "title": "Nginx Stream orqali SOCKS5 / TCP tunnel shlyuzini amalga oshirish",
        "desc": "Tashqi dunyoga to'g'ridan-to'g'ri chiqish huquqiga ega bo'lmagan ichki mikroxizmatlar uchun xavfsiz SOCKS5 proksi shlyuzi talab qilinadi.",
        "req": "SOCKS5 handshake (0x05, 1 metod, 0x00 no-auth), ulanish buyrug'i (CMD 0x01 Connect), manzil turi bo'yicha IP/Domen va portni o'qish, ulanishni ulash.",
        "code": """-- SOCKS5 Proksi protokoli tekshiruvchisi
local _M = {}

function _M.handle_socks5(client_sock)
    -- 1. Handshake qabul qilish: VER (1) + NMETHODS (1) + METHODS (N)
    local ver_data, err = client_sock:receive(2)
    if not ver_data then return end
    
    local ver, nmethods = string.unpack(">I1I1", ver_data)
    if ver ~= 0x05 then return client_sock:close() end
    
    local methods = client_sock:receive(nmethods)
    -- 0x05 (SOCKS5), 0x00 (Autentifikatsiyasiz javob)
    client_sock:send(string.pack(">I1I1", 0x05, 0x00))
    
    -- 2. Request details: VER, CMD, RSV, ATYP
    local req_header = client_sock:receive(4)
    local _, cmd, _, atyp = string.unpack(">I1I1I1I1", req_header)
    
    local target_host, target_port
    if atyp == 0x01 then -- IPv4 (4 bayt)
        local ip_bytes = client_sock:receive(4)
        target_host = string.format("%d.%d.%d.%d", string.byte(ip_bytes, 1, 4))
    end
    
    local port_bytes = client_sock:receive(2)
    target_port = string.unpack(">I2", port_bytes)
    
    ngx.log(ngx.INFO, "SOCKS5 Tunnel so'rovi: ", target_host, ":", target_port)
    -- Muvaffaqiyatli javob: 0x05, 0x00, 0x00, 0x01 + 0.0.0.0:0
    client_sock:send(string.pack(">I1I1I1I1I4I2", 0x05, 0x00, 0x00, 0x01, 0, 0))
end

return _M""",
        "expl": "SOCKS5 quyi darajadagi TCP tunnellash standarti bo'lib, har qanday protokol (HTTP, SSH, SMTP) bilan ishlaydi. OpenResty cosocket orqali SOCKS5 implementatsiyasi yuqori tezlik va past resurs sarfi bilan korporativ xavfsizlik shlyuzlarini yaratishga imkon beradi."
    },
    {
        "id": 1119,
        "title": "Nginx Stream UDP asosidagi keshlovchi DNS proksi shlyuzi",
        "desc": "Korxona ichidagi minglab serverlarning DNS so'rovlarini tashqi DNS serveriga har safar yuborib vaqt yo'qotmaslik uchun UDP darajasidagi tezkor keshlovchi shlyuz kerak.",
        "req": "`ngx.req.socket()` orqali UDP paketini olish, DNS savol xeshini `lua_shared_dict` dan izlash, keshda bo'lsa darhol qaytarish, bo'lmasa upstreamga uzatib keshga yozish.",
        "code": """-- UDP DNS Caching Gateway
local dns_cache = ngx.shared.dns_cache
local client_sock = ngx.req.socket()

local request_packet, err = client_sock:receive()
if not request_packet or #request_packet < 12 then
    return ngx.exit(ngx.ERROR)
end

-- DNS Transaction ID (dastlabki 2 bayt)
local tx_id = string.sub(request_packet, 1, 2)
local question_data = string.sub(request_packet, 13) -- Savol qismi

local cached_response = dns_cache:get(question_data)
if cached_response then
    -- Keshdagi javobning Transaction ID sini mijoznikiga almashtiramiz
    local final_packet = tx_id .. string.sub(cached_response, 3)
    client_sock:send(final_packet)
    return
end

-- Upstream 8.8.8.8 ga so'rov jo'natish
local upstream = ngx.socket.udp()
upstream:setpeername("8.8.8.8", 53)
upstream:send(request_packet)
local response_packet = upstream:receive()

if response_packet then
    dns_cache:set(question_data, response_packet, 60) -- 60 soniya kesh
    client_sock:send(response_packet)
end""",
        "expl": "DNS paketining birinchi 2 bayti tranzaksiya ID si bo'lib, har bir so'rovda o'zgaradi, lekin uning savol tanasi bir xil bo'ladi. DNS savolini kalit qilib keshlashtirish va faqat Transaction ID ni almashtirib qaytarish so'rovlarga 0.1 ms ichida javob berishni ta'minlaydi."
    },
    {
        "id": 1120,
        "title": "Stream ulanishlarining trafigi (kiruvchi va chiquvchi baytlar) va davomiyligi bo'yicha hisoblagich (Accounting)",
        "desc": "Bulutli xizmatlarda har bir mijoz yoki ijarachi (tenant) qancha tarmoq trafigini sarflaganini aniq hisoblab borish va belgilangan kvotadan oshganda xizmatni cheklash talab etiladi.",
        "req": "`log_by_lua_block` da `ngx.var.bytes_received`, `ngx.var.bytes_sent` va `ngx.var.session_time` o'zgaruvchilarini hisobga olish va statistikani yangilash.",
        "code": """-- Stream log_by_lua_block da trafik hisob-kitobi
local tenant_id = ngx.var.remote_addr -- Yoki autentifikatsiyadan olingan identifikator
local bytes_in = tonumber(ngx.var.bytes_received) or 0
local bytes_out = tonumber(ngx.var.bytes_sent) or 0
local session_duration = tonumber(ngx.var.session_time) or 0

local accounting = ngx.shared.tenant_accounting

-- Kiruvchi va chiquvchi trafikni atomar oshirish
accounting:incr(tenant_id .. ":in", bytes_in, 0)
accounting:incr(tenant_id .. ":out", bytes_out, 0)
accounting:incr(tenant_id .. ":duration", session_duration, 0)

ngx.log(ngx.INFO, string.format("Tenant [%s] sessiya yakuni: %d bayt kirdi, %d bayt chiqdi, davomiyligi: %.2f sek", 
    tenant_id, bytes_in, bytes_out, session_duration))""",
        "expl": "`log_by_lua_block` sessiya to'liq yakunlangach, barcha resurslar yopilgan vaqtda chaqiriladi. Undagi statistik ma'lumotlar to'liq va aniq bo'ladi. `shared_dict:incr` atomar bajarilgani sababli barcha workerlar bitta hisoblagichni xavfsiz yangilaydi."
    },
    {
        "id": 1121,
        "title": "resty.redis orqali Redisga ulanish, buyruqlar bajarish va keepalive hovuziga qaytarish",
        "desc": "OpenResty ilovalarida Redis bilan o'zaro aloqa yuqori darajada tezkor bo'lishi va har bir operatsiyadan keyin ulanish hovuziga to'g'ri qaytarilishi shart.",
        "req": "`resty.redis` modulidan foydalanish, autentifikatsiya, ma'lumot yozish/o'qish, xatoliklarni tekshirish va `set_keepalive` qilish.",
        "code": """-- Yuqori unumdor Redis mijozi
local redis = require "resty.redis"
local _M = {}

function _M.get_cached_value(key)
    local red = redis:new()
    red:set_timeouts(1000, 2000, 2000) -- 2 soniya timeout
    
    local ok, err = red:connect("127.0.0.1", 6379)
    if not ok then
        return nil, "Redisga ulanish xatosi: " .. tostring(err)
    end
    
    -- Qiymatni olish
    local res, get_err = red:get(key)
    if not res then
        red:close()
        return nil, "GET xatosi: " .. tostring(get_err)
    end
    
    if res == ngx.null then
        res = nil -- Kalit mavjud emas
    end
    
    -- Ulanishni hovuzga qaytarish (10 soniya idle, 100 ta ulanish hovuzi)
    local keepalive_ok, keepalive_err = red:set_keepalive(10000, 100)
    if not keepalive_ok then
        ngx.log(ngx.WARN, "Keepalive xatosi: ", keepalive_err)
        red:close()
    end
    
    return res, nil
end

return _M""",
        "expl": "OpenResty da `res == ngx.null` tekshiruvi muhimdir, chunki Redis `nil` qiymat qaytarganda Lua ning oddiy `nil` qiymatidan farqlash uchun `ngx.null` maxsus yengil obyektidan foydalaniladi. `set_keepalive` esa ulanishni keyingi so'rovlar uchun ochiq qoldiradi."
    },
    {
        "id": 1122,
        "title": "Redis Pipelining yordamida yuzlab buyruqlarni bitta TCP RTT orqali bajarish",
        "desc": "Bitta foydalanuvchi so'rovi davomida Redisga 50 ta alohida buyruq (masalan, har xil kalitlarni olish) yuborish 50 ta tarmoq kechikishini (RTT) keltirib chiqaradi.",
        "req": "`red:init_pipeline()` dan foydalanish, barcha buyruqlarni navbatga qo'yish, `red:commit_pipeline()` orqali bitta paketda jo'natish va natijalarni massivda olish.",
        "code": """-- Redis Pipelining orqali ommaviy so'rovlar
local redis = require "resty.redis"
local _M = {}

function _M.batch_fetch_profiles(user_ids)
    local red = redis:new()
    red:set_timeout(3000)
    local ok, err = red:connect("127.0.0.1", 6379)
    if not ok then return nil, err end
    
    -- Pipeliningni boshlash
    red:init_pipeline()
    for _, uid in ipairs(user_ids) do
        red:hgetall("user:" .. uid)
    end
    
    -- Barcha buyruqlarni bitta tarmoq so'rovida jo'natish
    local results, commit_err = red:commit_pipeline()
    if not results then
        red:close()
        return nil, "Pipeline xatosi: " .. tostring(commit_err)
    end
    
    red:set_keepalive(10000, 50)
    
    local profiles = {}
    for i, profile_data in ipairs(results) do
        if profile_data ~= ngx.null and type(profile_data) == "table" then
            profiles[user_ids[i]] = red:array_to_hash(profile_data)
        end
    end
    
    return profiles, nil
end

return _M""",
        "expl": "Redis Pipelining tarmoqning uzatish tezligini (throughput) 10-20 baravargacha oshiradi. Har bir buyruq uchun tarmoq paketi ketmaydi, balki operatsion tizimning TCP buferida barcha buyruqlar bitta katta MTU paketiga jamlanib uzatiladi va server ham barcha javoblarni bitta oqimda qaytaradi."
    },
    {
        "id": 1123,
        "title": "Redis Tranzaksiyalari (MULTI/EXEC) va atomar buyruqlar ketma-ketligi",
        "desc": "Moliya yoki balans o'zgarishi bilan bog'liq amallarda bir nechta Redis kalitlari boshqa mijozlar aralashuvisiz atomar yangilanishi shart.",
        "req": "`red:multi()`, operatsiyalarni navbatga qo'yish, `red:exec()` orqali tasdiqlash, tranzaksiya bekor bo'lsa (abort) holatni qaytarish.",
        "code": """-- Redis Tranzaksiyalari (MULTI/EXEC)
local redis = require "resty.redis"
local _M = {}

function _M.transfer_balance(from_user, to_user, amount)
    local red = redis:new()
    red:set_timeout(2000)
    local ok, err = red:connect("127.0.0.1", 6379)
    if not ok then return false, err end
    
    -- Tranzaksiyani boshlash
    red:multi()
    red:decrby("balance:" .. from_user, amount)
    red:incrby("balance:" .. to_user, amount)
    
    -- Tranzaksiyani atomar bajarish
    local replies, exec_err = red:exec()
    if not replies then
        red:close()
        return false, "Tranzaksiya rad etildi: " .. tostring(exec_err)
    end
    
    red:set_keepalive(10000, 20)
    return true, nil
end

return _M""",
        "expl": "`MULTI/EXEC` buyruqlari blokidagi operatsiyalar Redis serverida oraliq to'xtovsiz, boshqa so'rovlar kiritilmasdan to'liq atomar bajariladi. Agar tranzaksiya o'rtasida xatolik yuz bersa, hech qanday qisman holat yuzaga kelmaydi."
    },
    {
        "id": 1124,
        "title": "Cosocket orqali Redis Pub/Sub kanaliga obuna bo'lish (SUBSCRIBE) va xabarlarni oqimli qabul qilish",
        "desc": "Haqiqiy vaqt rejimida yangilanuvchi konfiguratsiyalar yoki xabarlarni barcha Nginx workerlariga darhol yetkazish uchun Redis Pub/Sub kanalini doimiy tinglab turish lozim.",
        "req": "`red:subscribe()` dan foydalanish, cheksiz siklda `read_reply()` orqali yangi xabarlarni olish, keepalive ishlatmaslik (chunki obuna ochiq qoladi).",
        "code": """-- Redis Pub/Sub xabar iste'molchisi
local redis = require "resty.redis"
local _M = {}

function _M.listen_channel(channel_name, message_handler)
    local red = redis:new()
    red:set_timeout(0) -- Cheksiz kutish (timeout bo'lmaydi)
    
    local ok, err = red:connect("127.0.0.1", 6379)
    if not ok then return nil, err end
    
    local res, sub_err = red:subscribe(channel_name)
    if not res then
        red:close()
        return nil, sub_err
    end
    
    ngx.log(ngx.INFO, "Kanalga obuna bo'lindi: ", channel_name)
    
    while true do
        -- Yangi xabarni asinxron kutish
        local msg, read_err = red:read_reply()
        if not msg then
            ngx.log(ngx.ERR, "Pub/Sub xatolik: ", read_err)
            break
        end
        
        -- msg formati: {"message", channel, data}
        if msg[1] == "message" then
            local payload = msg[3]
            message_handler(payload)
        end
    end
    
    red:close()
end

return _M""",
        "expl": "Pub/Sub rejimiga o'tgan Redis ulanishi odatiy buyruqlarni qabul qilmaydi, faqat obuna xabarlarini tinglaydi. Shu sababli bu soketga `set_keepalive()` qilinmaydi va alohida fon korutinasida (`ngx.thread.spawn` yoki `ngx.timer.at`) ushlab turiladi."
    },
    {
        "id": 1125,
        "title": "Redis Sentinel orqali master server manzilini dinamik aniqlash va failoverni boshqarish",
        "desc": "Yuqori bardoshli (High Availability) tizimlarda Redis master serveri avariyaga uchrasa, Sentinel yangi masterni saylaydi. Ilova avtomatik tarzda yangi masterga ulanishi kerak.",
        "req": "Sentinel tuguniga ulanish, `sentinel get-master-addr-by-name` buyrug'ini bajarish, olingan IP va port bilan masterga ulanish.",
        "code": """-- Redis Sentinel orqali Master manzilini topuvchi modul
local redis = require "resty.redis"
local _M = {}

function _M.get_master_address(sentinel_host, sentinel_port, master_name)
    local red = redis:new()
    red:set_timeout(1000)
    
    local ok, err = red:connect(sentinel_host, sentinel_port)
    if not ok then return nil, nil, err end
    
    -- Sentinel buyrug'i: SENTINEL get-master-addr-by-name <name>
    local res, cmd_err = red:sentinel("get-master-addr-by-name", master_name)
    if not res or res == ngx.null then
        red:close()
        return nil, nil, "Master topilmadi: " .. tostring(cmd_err)
    end
    
    red:set_keepalive(10000, 10)
    
    local master_ip = res[1]
    local master_port = tonumber(res[2])
    return master_ip, master_port, nil
end

return _M""",
        "expl": "Sentinel arxitekturasi dasturchilarga Redis ulanish manzilini kodda qattiq belgilamaslik (hardcode) imkonini beradi. Avariya (failover) paytida OpenResty Sentinel orqali yangi masterni soniyaning ulushlarida aniqlab, so'rovlarni uzluksiz yangi nodega yo'naltiradi."
    }
]
